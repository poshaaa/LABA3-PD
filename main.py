from PyQt5 import uic
from PyQt5.Qt import QPushButton, QLineEdit, QWidget, QVBoxLayout, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
import json
from gost import *

# Форма регистрации и входа
LoginForm, LoginWindow = uic.loadUiType("LoginForm.ui")
app = QApplication([])
loginWindow = LoginWindow()
loginForm = LoginForm()
loginForm.setupUi(loginWindow)
# Форма шифрования и дешифрования
CipherForm, CipherWindow = uic.loadUiType("CipherForm.ui")
cipherWindow = CipherWindow()
cipherForm = CipherForm()
cipherForm.setupUi(cipherWindow)
# Форма для возвращения к прошлым окнам
BTUForm, BTUWindow = uic.loadUiType("BTUForm.ui")
BTUWindow = BTUWindow()
BTUForm = BTUForm()
BTUForm.setupUi(BTUWindow)

loginWindow.show()


# Функции для смены и возвращения форм
def formOpen_1():
    cipherWindow.show()
    loginWindow.close()


def formOpen_2():
    BTUWindow.show()
    cipherWindow.close()


def formReturn_1():
    loginWindow.show()
    BTUWindow.close()


def formReturn_2():
    cipherWindow.show()
    BTUWindow.close()


# Загрузка списка пользователей
usersList = {}
try:
    with open('users/userList.json') as json_file:
        usersList = json.load(json_file)
except Exception:
    with open('users/userList.json', 'w') as outfile:
        usersList = {"users": []}
        json.dump(usersList, outfile)

# Авторизация
inputLogin = ""
inputPassword = ""


def signUp():
    if len(loginForm.UserNamelineEdit.text()) > 0 and len(loginForm.PasswordlineEdit.text()) > 0:
        inputLogin = loginForm.UserNamelineEdit.text()
        inputPassword = loginForm.PasswordlineEdit.text()
        userCreate(inputLogin, inputPassword)


def signIn():
    if len(loginForm.UserNamelineEdit.text()) > 0 and len(loginForm.PasswordlineEdit.text()) > 0:
        inputLogin = loginForm.UserNamelineEdit.text()
        inputPassword = loginForm.PasswordlineEdit.text()
        isUserExist = False
        neededPassword = ""
        for x in range(len(usersList["users"])):
            if (usersList["users"][x]["login"] == inputLogin):
                isUserExist = True
                neededPassword = usersList["users"][x]["password"]
                break
        if not isUserExist or inputPassword != neededPassword:
            pixmap = QPixmap('loser.png')
            loginForm.status_label.setPixmap(pixmap)
            loginForm.status_label_text.setText("Вы не зарегистрированы")
        elif isUserExist and inputPassword == neededPassword:
            pixmap = QPixmap('win.png')
            loginForm.status_label.setPixmap(pixmap)
            loginForm.status_label_text.setText("Успешный вход")
            formOpen_1()
            cipherForm.label_username.setText(format(inputLogin))
    else:
        pixmap = QPixmap('empty.png')
        loginForm.status_label.setPixmap(pixmap)
        loginForm.status_label_text.setText("Введите данные")


def userCreate(iL, iP):
    isUserExist = False
    # Проверка, есть ли пользователь
    if len(usersList["users"]) > 0:
        for x in range(len(usersList["users"])):
            if usersList["users"][x]["login"] == iL:
                pixmap = QPixmap('nopassword.png')
                loginForm.status_label.setPixmap(pixmap)
                loginForm.status_label_text.setText("Такой пользователь уже есть! ")
                isUserExist = True
                break
    else:
        loginForm.status_label.setText("Пустые поля")
    if not isUserExist:
        usersList["users"].append({"login": iL, "password": iP})
        with open('users/userList.json', 'w') as outfile:
            json.dump(usersList, outfile)
            pixmap = QPixmap('win.png')
            loginForm.status_label.setPixmap(pixmap)
            loginForm.status_label_text.setText("Регистрация успешна")
            formOpen_1()
            cipherForm.label_username.setText(format(iL))


loginForm.LogInpushButton.clicked.connect(signUp)
loginForm.LogUppushButton.clicked.connect(signIn)

# шифрование и дешифрование

cipher = GOST28147_89()


def cipherMessage(txt):
    key = [0xFFFFFFFF, 0x12345678, 0x00120477, 0x77AE441F, 0x81C63123, 0x99DEEEEE, 0x09502978, 0x68FA3105]
    g = 128 * 1024  # one MB
    strword = cipherForm.TextForCipherlineEdit.text()
    word = int(strword)
    for i in range(g):
        cipherresult = cipher.encrypt(word, key)
    uncipherresult = cipher.decrypt(cipherresult, key)
    cipherresult = str(cipherresult)
    cipherForm.CipherDolineEdit.setText(cipherresult)
    uncipherresult = str(uncipherresult)
    cipherForm.UnCipherDolineEdit.setText(uncipherresult)
    outputFile = "Ключ колонок: {0}\nКлючевое слово: {1}".format(key, word)
    with open("cipherMessage.txt", "w") as file:
        file.write(outputFile)


# функция для очищения полей при возвращении на форму с шифрованием

def clear():
    cipherForm.TextForCipherlineEdit.setText('')
    cipherForm.CipherDolineEdit.setText('')
    cipherForm.UnCipherDolineEdit.setText('')


cipherForm.CipherDopushButton.clicked.connect(cipherMessage)
cipherForm.pushButton.clicked.connect(formOpen_2)
BTUForm.mainreturnpushButton.clicked.connect(formReturn_1)
BTUForm.cipherreturnpushButton.clicked.connect(formReturn_2)
BTUForm.cipherreturnpushButton.clicked.connect(clear)
BTUForm.mainreturnpushButton.clicked.connect(clear)
app.exec_()
