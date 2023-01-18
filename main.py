import sys
from PyQt5.QtWidgets import QApplication
from auth import AuthDialog
from cypher import Morse

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthDialog()
    window.show()
    sys.exit(app.exec_())
