# python 
# Created by Tuan Anh Phan on 31.05.2023
from PyQt5.QtWidgets import *
class Alert(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.Alert = QMessageBox()

    def Raise_Alert(self, Title, Icon, Text):
        self.Alert.setWindowTitle(Title)
        self.Alert.setIcon(Icon)
        self.Alert.setText(Text)
        self.Alert.setStandardButtons(QMessageBox.Ok)
        self.Alert.buttonClicked.connect(self.Alert.close)
        retval = self.Alert.exec_()

    def Raise_Warning(self):
        self.Raise_Alert("Ошибка", QMessageBox.Warning, "Вы не выбрали файл")

    def Raise_Information(self):
        self.Raise_Alert("Успешно", QMessageBox.Information, "Процесс измениение завершен")

    def Raise_Critical(self):
        self.Raise_Alert("Ошибка", QMessageBox.Critical, "Вы не выбрали папку")

    def Raise_Not_Encrypt_File(self):
        self.Raise_Alert("Ошибка", QMessageBox.Warning, "Выбрали незашифрованное слово")

    def Raise_Critical_Start(self):
        self.Raise_Alert("Ошибка", QMessageBox.Critical, "ОШИБКА, ПРОВЕРЯЙТЕ ФАЙЛ config.txt")


if __name__ == '__main__':
    pass
