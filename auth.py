from PyQt5.QtWidgets import QMainWindow, QDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import base64
import game
from cypher import *
import register


class AuthDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checkers | Авторизация")
        self.setFixedSize(500, 300)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

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
        self.label.setGeometry(QtCore.QRect(0, 0, 500, 50))
        self.label.setFont(self.def_font)
        self.label.setObjectName("label")
        self.label.setText("Вход")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Inputs
        self.loginInput = QtWidgets.QLineEdit(self)
        self.loginInput.setGeometry(QtCore.QRect(170, 60, 160, 25))
        self.loginInput.setObjectName("loginInput")
        self.loginInput.setPlaceholderText("Логин")

        self.passInput = QtWidgets.QLineEdit(self)
        self.passInput.setGeometry(QtCore.QRect(170, 90, 160, 25))
        self.passInput.setObjectName("passInput")
        self.passInput.setPlaceholderText("Пароль")

        # Buttons
        self.loginBtn = QtWidgets.QPushButton(self)
        self.loginBtn.setGeometry(QtCore.QRect(170, 125, 160, 50))
        self.loginBtn.setText("Войти")

        self.signupBtn = QtWidgets.QPushButton(self)
        self.signupBtn.setGeometry(QtCore.QRect(170, 175, 160, 25))
        self.signupBtn.setText("Регистрация")

        # Finally
        self.registerBtns()

    @QtCore.pyqtSlot()
    def registerBtnHandler(self):
        self.register_wind = register.SignUp()
        self.register_wind.show()

    @QtCore.pyqtSlot()
    def loginBtnHandler(self):
        login = Morse.encrypt(self.loginInput.text())
        password = Morse.encrypt(self.passInput.text())
        if not login or not password:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля!')
            return
        with open('accounts.txt', 'r') as f:
            data = f.read()
        if data is not None:
            rows = data.split('\n')
            accounts = [x.split('  ') for x in rows]
            account_data = None
            for k in accounts:
                if len(k) == 3:
                    if k[0].strip().rstrip() == login.strip().rstrip():
                        account_data = k
            if account_data is not None:
                if account_data[1].strip().rstrip() == password.strip().rstrip():
                    self.close()
                    game.run()
                else:
                    QtWidgets.QMessageBox.information(self, 'Внимание!', 'Неверный пароль')
            else:
                QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь не найден')
        else:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь не найден')

    def registerBtns(self):
        self.signupBtn.clicked.connect(self.registerBtnHandler)
        self.loginBtn.clicked.connect(self.loginBtnHandler)