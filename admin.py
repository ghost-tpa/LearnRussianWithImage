# python 3.7
# Created by Tuan Anh Phan on 01.11.2022
# DONE 28.01.2023
from os import getcwd as os_getcwd
from os import path as os_path
from os import walk as os_walk
from os import chdir as os_chdir
from sys import argv as sys_argv
from sys import exit as sys_exit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from bytearray_kunheztrik import func_RKey
from bytearray_text_kuz import blockEncrypt
from Alert import Alert


MAX_FRAME_W = 100
MAX_FRAME_H = 100

# TODO: thêm mark vào file encrypt

os_chdir(os_path.join(os_getcwd(), "src"))  # change dict to src folder

config_check_file_path = os_path.join(os_getcwd(), "config_path_file.txt")
data_file_check = open(config_check_file_path, "r", encoding='utf-8').read()
if data_file_check == "":
    config_file_path = os_path.join(os_getcwd(), "config.txt")
else:
    config_file_path = data_file_check

arr_data_config = open(config_file_path, "r", encoding='utf-8').read().split("\n")


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.RAISE = Alert()  # from class Alert raise QMessageBox alert

        self.setMinimumSize(1366, 768)
        self.setWindowTitle("Administrator Tools, Инструменты администратора")
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        key = "xinchaovietnam123455432100000000"
        self.rKey = func_RKey(bytearray(key.encode()))
        self.protect()

    def diag_choose_config_file(self):
        # this diag is created for syns data in internet env
        self.diag_config_file = QDialog()
        diag_config_file = QFormLayout()
        self.diag_config_file.setLayout(diag_config_file)
        fileName, _ = QFileDialog.getOpenFileName(self, "Окрыть файловый текст", "", "Text file (*.txt)")

        retval = self.diag_config_file.exec_()

    def protect(self):
        self.dial_protect = QDialog()
        self.dial_protect.setMinimumSize(512, 512)
        self.dial_protect.setStyleSheet("background-image: url(lock.png)")
        dial_protect_layout = QFormLayout()
        self.dial_protect.setLayout(dial_protect_layout)
        self.ledit_password = QLineEdit()
        self.ledit_password.setStyleSheet("background-color: yellow;")
        self.ledit_password.setMinimumSize(200, 50)
        self.ledit_password.setEchoMode(QLineEdit.Password)
        self.ledit_password.returnPressed.connect(self.check_password)
        self.ledit_password.setPlaceholderText("Введите пароль")
        dial_protect_layout.addWidget(self.ledit_password)

        enter_button = QPushButton("ОК")
        enter_button.clicked.connect(self.check_password)
        dial_protect_layout.addWidget(enter_button)
        # IKCI2023
        # 033d4df0f87c6a84658a6659dd18efd3
        retval = self.dial_protect.exec_()

    def check_password(self):
        # embedding password in the code
        # it's so fucking dummy but im too lazy to fix it

        if blockEncrypt(self.rKey,
                        bytearray(self.ledit_password.text().encode())).hex() == "aa98196ed8af991d1ff2e89b0ddc936e":  # xinchaovietnam
            self.dial_protect.close()
            try:
                self.UI_config()
            except:
                self.RAISE.Raise_Critical_Start()
                exit(0)
        else:
            self.ledit_password.setText("")

    def UI_config(self):
        self.button_add_new = QPushButton("Зашифровать слова")
        self.button_add_new.clicked.connect(self.return_clicked_button_add_new)
        self.layout.addWidget(self.button_add_new, 0, 0)

        self.main_frame = QFrame()
        self.main_frame.setMaximumSize(MAX_FRAME_W, MAX_FRAME_H)

        self.main_frame.setMinimumSize(1000, 300)
        self.layout.addWidget(self.main_frame, 1, 0)

        self.main_frame_layout = QGridLayout()
        self.main_frame.setLayout(self.main_frame_layout)
        self.frame_config()

        button_exit = QPushButton("Выход")
        button_exit.clicked.connect(self.on_clicked_exit_button)
        self.layout.addWidget(button_exit, 2, 0)

    def on_clicked_exit_button(self):
        self.return_clicked_button_save_config()
        exit(0)

    def frame_config(self):
        self.lst_data_config = self.get_data_from_file()

        self.config_font = QLabel("Шрифт")
        self.main_frame_layout.addWidget(self.config_font, 0, 0)
        self.ledit_config_font = QLineEdit(self.lst_data_config[0].split("=")[1])
        self.ledit_config_font.setReadOnly(True)
        self.main_frame_layout.addWidget(self.ledit_config_font, 0, 1)

        self.config_font_size = QLabel("Размер букв")
        self.main_frame_layout.addWidget(self.config_font_size, 1, 0)
        self.spbox_config_font_size = QSpinBox()
        self.spbox_config_font_size.setValue(int(self.lst_data_config[1].split("=")[1]))
        self.main_frame_layout.addWidget(self.spbox_config_font_size, 1, 1)


        self.config_data_file_path = QLabel("Выбрать слово")
        self.main_frame_layout.addWidget(self.config_data_file_path, 2, 0)
        lst_file_path = self.lst_data_config[2].split("=")
        self.cbbox_config_data_file_path = QComboBox()
        self.cbbox_config_data_file_path.insertItem(0, self.lst_data_config[2].split("=")[1])
        for _, _, filenames in os_walk(os_path.join(os_getcwd(), "data")):
            for filename in filenames:
                if filename != self.lst_data_config[2].split("=")[1]:
                    self.cbbox_config_data_file_path.addItem(filename)
        self.main_frame_layout.addWidget(self.cbbox_config_data_file_path, 2, 1)
        self.button_change_dict = QPushButton("Изменить")
        self.button_change_dict.clicked.connect(self.return_clicked_button_change_dict)
        self.main_frame_layout.addWidget(self.button_change_dict, 2, 2)


        self.config_img_file_path = QLabel("Место хранения рисунока, соответствующего слову")
        self.main_frame_layout.addWidget(self.config_img_file_path, 3, 0)
        self.ledit_config_img_file_path = QLineEdit(self.lst_data_config[3].split("=")[1])
        self.main_frame_layout.addWidget(self.ledit_config_img_file_path, 3, 1)
        self.button_change_folder_photo = QPushButton("Изменить")
        self.button_change_folder_photo.clicked.connect(self.return_clicked_button_change_folder_photo)
        self.main_frame_layout.addWidget(self.button_change_folder_photo, 3, 2)

        self.config_res_file_path = QLabel("Место хранения результатов слушателей")
        self.main_frame_layout.addWidget(self.config_res_file_path, 4, 0)
        self.ledit_config_res_file_path = QLineEdit(self.lst_data_config[4].split("=")[1])
        self.ledit_config_res_file_path.setReadOnly(True)
        self.main_frame_layout.addWidget(self.ledit_config_res_file_path, 4, 1)

        self.config_num_ques = QLabel("Количество вопросов")
        self.main_frame_layout.addWidget(self.config_num_ques, 5, 0)
        self.spbox_config_num_ques = QSpinBox()

        self.spbox_config_num_ques.setValue(int(self.lst_data_config[5].split("=")[1]))
        self.main_frame_layout.addWidget(self.spbox_config_num_ques, 5, 1)

        self.pbut_config_save = QPushButton("Сохранить")
        self.pbut_config_save.clicked.connect(self.return_clicked_button_save_config)
        self.main_frame_layout.addWidget(self.pbut_config_save, 6, 1)

    def return_clicked_button_add_new(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Открыть файловый текст", os_path.join(os_getcwd(),
                                                                                     "data"), "Text file (*.txt)")
        print("filename = ", fileName)
        if fileName == '':
            self.RAISE.Raise_Warning()

        else:
            f_obj = open(fileName, 'r', encoding='utf-8')
            lst_data = f_obj.read().split("\n")
            f_obj.close()
            while "" in lst_data:
                lst_data.remove("")
            if os_path.isfile(fileName.replace(".txt", "_encrypted.txt")):
                f_obj = open(fileName.replace(".txt", "_encrypted_1.txt"), 'w', encoding='utf-8')
            else:
                f_obj = open(fileName.replace(".txt", "_encrypted.txt"), 'w', encoding='utf-8')
            f_obj.write("ENCRYPTED_\n")
            for data in lst_data:
                f_obj.write(blockEncrypt(self.rKey, bytearray(data.encode())).hex() + "\n")
            f_obj.close()
            self.RAISE.Raise_Information()


    def return_clicked_button_change_dict(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Окрыть файловый текст", os_path.join(os_getcwd(),
                                                                                              "data"), "Text file (*.txt)")
        if fileName == '':
            self.RAISE.Raise_Warning()
        else:
            lst_data_from_file = open(fileName, 'r', encoding='utf-8').read().split("\n")
            if lst_data_from_file[0] != "ENCRYPTED_":
                self.RAISE.Raise_Not_Encrypt_File()
                self.return_clicked_button_change_dict()
            else:
                self.cbbox_config_data_file_path.setCurrentText(fileName.split(os_path.sep).pop())

    def return_clicked_button_change_folder_photo(self):
        try:
            folderName = QFileDialog.getExistingDirectory(self, "выбрать папку", os_path.join(os_getcwd(), "image"), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            if folderName == '':
                self.RAISE.Raise_Warning()
            else:
                self.ledit_config_img_file_path.setText(folderName.split(os_path.sep).pop())
        except:
            self.RAISE.Raise_Critical()

    def return_clicked_button_save_config(self):
        f_obj = open(config_file_path, "w", encoding='utf-8')

        lst_temp = self.lst_data_config[1].split("=")
        lst_temp[1] = str(self.spbox_config_font_size.value())
        self.lst_data_config[1] = "=".join(lst_temp)

        lst_temp = self.lst_data_config[2].split("=")
        lst_temp[1] = self.cbbox_config_data_file_path.currentText()
        self.lst_data_config[2] = "=".join(lst_temp)

        lst_temp = self.lst_data_config[3].split("=")
        lst_temp[1] = self.ledit_config_img_file_path.text()
        self.lst_data_config[3] = "=".join(lst_temp)

        lst_temp = self.lst_data_config[5].split("=")
        lst_temp[1] = str(self.spbox_config_num_ques.value())
        self.lst_data_config[5] = "=".join(lst_temp)

        for data in self.lst_data_config:
            f_obj.writelines(data + "\n")

        self.RAISE.Raise_Information()


    @staticmethod
    def get_data_from_file():
        file_obj = open(config_file_path, "r", encoding='utf-8')
        lst_res = file_obj.read().split("\n")
        file_obj.close()
        while "" in lst_res:
            lst_res.remove("")
        return lst_res


if __name__ == '__main__':
    app = QApplication(sys_argv)
    screen = Window()
    screen.show()
    sys_exit(app.exec_())

