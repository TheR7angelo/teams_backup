# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDateEdit, QGridLayout,
    QHBoxLayout, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

from Module.Widget.SliderToggle import PyToggle
from Interface import icon_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(284, 109)
        icon = QIcon()
        icon.addFile(u":/logo/asset/logo/TeamShit.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.but_valide_export = QPushButton(self.centralwidget)
        self.but_valide_export.setObjectName(u"but_valide_export")

        self.gridLayout.addWidget(self.but_valide_export, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 2, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 2, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.but_export_tout = QPushButton(self.centralwidget)
        self.but_export_tout.setObjectName(u"but_export_tout")
        self.but_export_tout.setCheckable(True)

        self.horizontalLayout.addWidget(self.but_export_tout)

        self.limit_date_active = PyToggle(self.centralwidget)
        self.limit_date_active.setObjectName(u"limit_date_active")

        self.horizontalLayout.addWidget(self.limit_date_active)

        self.limit_date = QDateEdit(self.centralwidget)
        self.limit_date.setObjectName(u"limit_date")
        self.limit_date.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.limit_date.sizePolicy().hasHeightForWidth())
        self.limit_date.setSizePolicy(sizePolicy)
        self.limit_date.setMinimumSize(QSize(83, 0))
        self.limit_date.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.limit_date.setDateTime(QDateTime(QDate(2022, 1, 1), QTime(0, 0, 0)))
        self.limit_date.setCalendarPopup(True)

        self.horizontalLayout.addWidget(self.limit_date)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 0, 1, 3)


        self.verticalLayout.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("")
        self.but_valide_export.setText(QCoreApplication.translate("MainWindow", u"Exporter", None))
        self.but_export_tout.setText(QCoreApplication.translate("MainWindow", u"Tout", None))
        self.limit_date_active.setText(QCoreApplication.translate("MainWindow", u"Date limite", None))
    # retranslateUi

