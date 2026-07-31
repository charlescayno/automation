# import sys
# from PyQt5.QtWidgets import QApplication, QWidget


# def main():

#     app = QApplication(sys.argv)

#     w = QWidget()
#     w.resize(1024, 768)
#     w.move(300, 150)
#     w.setWindowTitle('Lighting Automation')
#     w.show()

#     sys.exit(app.exec_())


# if __name__ == '__main__':
#     main()



import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Lighting Automation')
        self.setWindowIcon(QIcon('pi-logo.png'))

        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()