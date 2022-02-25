import sys
import os

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QSize, QPropertyAnimation, QDate, QThreadPool
from PySide6.QtGui import Qt, QFont, QScreen, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from Interface.mainWindow import Ui_MainWindow

from Interface import icon_rc

from fonction import get_liste_conversation
from worker import Worker


class mainWindow(QMainWindow, Ui_MainWindow):

    titre = 'TeamShit'

    def __init__(self, parent=None, groupes=None):
        super(mainWindow, self).__init__(parent)

        self.groupes = groupes

        self.setupUi(self)

        print(self.groupes)

        self.setup()
        self.setup_programme()
        self.setup_connection_button()

    def setup(self):
        def titre(self):
            font = QFont()
            font.setBold(True)

            # title = 'Extracteur photo'
            self.setWindowTitle(self.titre)

            # self.title.setText(self.titre)
            # self.title.setFont(font)

        def logo(self):
            icon = QIcon()
            icon.addFile(u":/logo/asset/logo/TeamShit.svg", QSize(), QIcon.Normal, QIcon.Off)
            self.setWindowIcon(icon)

        titre(self)
        logo(self)

        self.limit_date.setDate(QDate().currentDate())

    def setup_programme(self):

        self.threadpool = QThreadPool()

        self.limit_date_active._bg_color = '#DB1D00'
        self.limit_date_active._active_color = '#4FD971'
        self.limit_date_active._height = 100

        self.limit_date_active.stateChanged.connect(lambda: self.limit_date.setEnabled(self.limit_date_active.isChecked()))

        self.getlist()

    def setup_connection_button(self):
        self.but_valide_export.clicked.connect(self.export)

    def getlist(self):
        lister = Worker(fonction='lister')
        lister.signals.liste.connect(self.print_liste)
        self.threadpool.start(lister)

    def print_liste(self, liste):
        print(liste)

    def export(self):

        if self.but_export_tout.isChecked():
            fonction = 'tout'
        else:
            fonction = None

        self.worker = Worker(fonction=fonction)
        # self.worker.signals.data.connect(self.data_capft)

        self.threadpool.start(self.worker)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    SPL_Pixmap = QtGui.QPixmap(u":/logo/asset/logo/TeamShit.svg")
    splash = QtWidgets.QSplashScreen(SPL_Pixmap, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()

    locale = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    reptrad = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load("qtbase_" + locale, reptrad)  # qtbase_fr.qm
    app.installTranslator(translator)

    window = mainWindow(groupes=get_liste_conversation())
    splash.finish(window)
    window.show()
    sys.exit(app.exec())
