# python 
# Created by Tuan Anh Phan on 17.01.2023

from bytearray_kunheztrik import func_Encrypt, func_Decrypt, func_RKey

BYTES_LENGTH = 16
def main():  # for testing
    message = "xinchaovietnam"
    key = "xinchaovietnam123455432100000000"
    rKey = func_RKey(bytearray(key.encode()))
    byte_message = bytearray(message.encode())
    original_mess = byte_message[:]
    encrypted_mess = blockEncrypt(rKey, byte_message)
    print(encrypted_mess.hex())
    decrypted_mess = blockDecrypt(rKey, encrypted_mess)
    print(decrypted_mess == original_mess)

def padd(message: bytearray):  # PKCS #5
    if len(message) < BYTES_LENGTH:
        temp = BYTES_LENGTH - len(message)
        for i in range(temp):
            message += temp.to_bytes(1, 'big')
        return message
    else:
        temp = BYTES_LENGTH - (len(message) % BYTES_LENGTH)
        for i in range(temp):
            message += temp.to_bytes(1, 'big')
        return message

def unpad(message: bytearray):
    temp = message[-1]
    for _ in range(temp):
        message.pop()
    return message

def blockEncrypt(rKey: [bytearray], message: bytearray) -> bytearray:
    message = padd(message)
    num_block = len(message) // BYTES_LENGTH
    res = bytearray()
    for i in range(0, num_block):
        res.extend(func_Encrypt(rKey, message[i * BYTES_LENGTH: (i + 1) * BYTES_LENGTH]))
    return res

def blockDecrypt(rKey: [bytearray], message: bytearray) -> bytearray:
    num_block = len(message) // BYTES_LENGTH
    res = bytearray()
    for i in range(0, num_block):
        res.extend(func_Decrypt(rKey, message[i * BYTES_LENGTH: (i + 1) * BYTES_LENGTH]))
    return unpad(res)


if __name__ == '__main__':
    main()
