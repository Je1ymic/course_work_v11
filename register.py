from PyQt5.QtWidgets import QMainWindow, QDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import base64
from cypher import *


class SignUp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checkers | Регистрация")
        self.setFixedSize(400, 250)

        # Fonts init
        self.def_font = QtGui.QFont()
        self.def_font.setFamily("Tahoma")
        self.def_font.setPixelSize(25)
        self.def_font.setBold(True)
        self.def_font.setItalic(False)

        self.s_font = QtGui.QFont()
        self.s_font.setFamily("Arial")
        self.s_font.setPixelSize(16)
        self.s_font.setBold(False)
        self.s_font.setItalic(False)

        # Auth text label
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 400, 50))
        self.label.setFont(self.def_font)
        self.label.setObjectName("label")
        self.label.setText("Регистрация")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Inputs
        self.loginInput = QtWidgets.QLineEdit(self)
        self.loginInput.setGeometry(QtCore.QRect(120, 60, 160, 25))
        self.loginInput.setObjectName("loginInput")
        self.loginInput.setPlaceholderText("Логин")

        self.passInput = QtWidgets.QLineEdit(self)
        self.passInput.setGeometry(QtCore.QRect(120, 90, 160, 25))
        self.passInput.setObjectName("passInput")
        self.passInput.setPlaceholderText("Пароль")

        self.mailInput = QtWidgets.QLineEdit(self)
        self.mailInput.setGeometry(QtCore.QRect(120, 120, 160, 25))
        self.mailInput.setObjectName("mailInput")
        self.mailInput.setPlaceholderText("Почта")

        # Buttons
        self.signupBtn = QtWidgets.QPushButton(self)
        self.signupBtn.setGeometry(QtCore.QRect(120, 150, 160, 25))
        self.signupBtn.setText("Создать аккаунт")

        # Finally
        self.registerBtns()

    @QtCore.pyqtSlot()
    def registerBtnHandler(self):
        if self.loginInput.text() and self.passInput.text() and self.mailInput.text():
            login = Morse.encrypt(self.loginInput.text())
            password = Morse.encrypt(self.passInput.text())
            mail = Morse.encrypt(self.mailInput.text())
            with open('accounts.txt', 'r+') as f:
                data = f.read()

            accounts = []
            if data is not None:
                rows = data.split('\n')
                if len(rows) > 1:
                    if len(rows) != 0:
                        accounts = [x.split() for x in rows]

            if len(accounts) != 0:
                find = False
                for acc in accounts:
                    if len(acc) == 3:
                        if acc[0] == login:
                            find = True
                if find:
                    QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь с таким именем уже существует')
                else:
                    with open('accounts.txt', 'a+') as f:
                        f.write(login + '  ' + password + '  ' + mail + '\n')
                    self.close()
            else:
                with open('accounts.txt', 'a+') as f:
                    f.write(login + '  ' + password + '  ' + mail + '\n')
                self.close()
        else:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля!')

    def registerBtns(self):
        self.signupBtn.clicked.connect(self.registerBtnHandler)