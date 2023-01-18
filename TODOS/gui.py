# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import Qt
#
# class Main_Window(QMainWindow):
#
#     def __init__(self):
#         super(Main_Window, self).__init__()
#         self.setGeometry(50,50,800,800)
#         self.setWindowTitle("Usage Stats Lookup")
#         # self.setWindowIcon("icon.png")
#         self.home()
#         self.show()
#
#     def home(self):
#         layout = QHBoxLayout()
#         layout.addWidget(QComboBox())
#         Main_Window.setLayout(self,layout)
#
#
# app = QApplication([])
# GUI = Main_Window()
# GUI.show()
# app.exec_()

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Interface(QMainWindow):

    def __init__(self):
        super().__init__()
        self.app()

    def app(self):

        QIcon(r'C:\Dev\usage_data_0.0.1\data'
                 r'\reference\stupid_caterpie_thing.png')
        self.statusBar().showMessage('Made possible by '
            'https://smogon-usage-stats.herokuapp.com, created by user '
                                     'fingerprint at Smogon')


        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle('Pokemon Showdown Usage Stats')
        self.setWindowIcon(QIcon(r'C:\Dev\usage_data_0.0.1\data'
                                 r'\reference\stupid_caterpie_thing.png'))

        self._background()
        self._input_fields()
        self._menu_bar()

        self.show()

    def _background(self):
        p       = QPalette()
        grad    = QLinearGradient(10,25,35,400)
        grad.setColorAt(0.0, QColor(204, 153, 255))
        grad.setColorAt(1.0, QColor(153, 204, 255))
        p.setBrush(QPalette.Window, QBrush(grad))
        self.setPalette(p)

    def _menu_bar(self):
        menubar     = self.menuBar()
        fileMenu    = menubar.addMenu('Main')
        editMenu    = menubar.addMenu('Edit')
        newAct      = QAction('New', self)
        impMenu     = QMenu('Credits', self)
        editAct     = QAction('Clear', self)

        editMenu.addAction(editAct)
        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)

    def _input_fields(self):
        central_wid = QWidget()
        gen     = QLabel("Gen: ")
        tier    = QLabel("Tier: ")
        rating  = QLabel("Rating (0): ")
        gen_edit    = QLineEdit()
        tier_edit   = QLineEdit()
        rating_edit = QLineEdit()
        grid = QGridLayout()

        grid.setSpacing(10)
        grid.addWidget(gen, 1, 0)
        grid.addWidget(gen_edit, 1, 1)
        grid.addWidget(tier, 2, 0)
        grid.addWidget(tier_edit, 2, 1)
        grid.addWidget(rating, 3, 0)
        grid.addWidget(rating_edit, 3, 1)

        central_wid.setLayout((grid))
        self.setCentralWidget(central_wid)


        # layout.(300, 300, 350, 300)

    # class Errors(QWidget):
    #
    #     def __init__(self):
    #         QWidget.__init__(self)
    #         self._error_message()
    #
    #     def _error_message(self):
    #
    #
    #         okButton = QPushButton("OK")
    #         cancelButton = QPushButton("Cancel")
    #
    #         hbox = QHBoxLayout()
    #         hbox.addStretch(1)
    #         hbox.addWidget(okButton)
    #         hbox.addWidget(cancelButton)
    #
    #         vbox = QVBoxLayout()
    #         vbox.addStretch(1)
    #         vbox.addLayout(hbox)
    #
    #         self.setLayout(vbox)
    #
    #         self.setGeometry(300, 300, 300, 150)
    #         self.setWindowTitle('Error!')
    #         self.show()



if __name__ == '__main__':

    myapp = QApplication(sys.argv)
    ex = Interface()
    sys.exit(myapp.exec_())