# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class PyToggle(QCheckBox):
    def __init__(self,
                 witdh=60,
                 height=28,
                 bg_color='#777',
                 circle_color='#DDD',
                 active_color="#00BCFF",
                 animation_curve=QEasingCurve.OutBounce,
                 duration=500):
        QCheckBox.__init__(self)

        # SET DEFAULT PARAMETERS
        self.setFixedSize(witdh, height)
        self.setCursor(Qt.PointingHandCursor)

        # COLORs
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        # CREATE ANIMATION
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(duration)  # Time in milliseconds

        # CONNECT STAT CHANGED
        # self.stateChanged.connect(self.debug)
        self.stateChanged.connect(self.start_transition)

    # CREATE NEW SET AND PROPERTY
    # @pyqtProperty(float)
    @Property(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = int(pos)
        self.update()

    def start_transition(self, value):
        self.animation.stop()  # Stop animation is running
        if value:
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(3)

        # START ANIMATION
        self.animation.start()

        # statue = self.isChecked()
        # print("Statut: " + str(statue))

    # SET NEW HIT AREA
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        # SET PAINTER
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # SET AS NO PEN
        p.setPen(Qt.NoPen)

        # DRAW RECTANGLE
        rect = QRect(0, 0, self.width(), self.height())

        # CHECK IF IS CHECKED
        if not self.isChecked():
            # DRAW BG
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            # DRAW CIRCLE
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)
        else:
            # DRAW BG
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            # DRAW CIRCLE
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)

        # END DRAW
        p.end()


class PyCircularProgress(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        # CUSTOM PROPERTY
        self.shadow = None
        self.value = 0
        self.width = 0
        self.height = 0
        self.progress_width = 10
        self.progress_rounded_cap = True
        self.progress_color = 0x498BD1
        self.max_value = 100
        self.font_family = "Segoe UI"
        self.font_size = 12
        self.suffix = '%'
        self.text_color = 0x498BD1
        self.enable_shadow = True

        # DEFAULT SIZE VALUE WITHOUT LAYOUT
        self.resize(self.width, self.height)

    # ADD SHADOW
    def add_shadow(self, enable):
        if enable:
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 120))
            self.setGraphicsEffect(self.shadow)

    # SET VALUE
    def set_value(self, value):
        self.value = value
        self.repaint()

    # PAINT EVENT
    def paintEvent(self, event):
        # SET PROGRESS PARAMETER
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value

        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setFont(QFont(self.font_family, self.size))

        # CREATE RECTANGLE
        rect = QRect(0, 0, self.width, self.height)
        p.drawRect(rect)

        # PEN
        pen = QPen()
        pen.setColor(QColor(self.progress_color))
        pen.setWidth(self.progress_width)

        # SET ROUND CAP
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)

        # CREATE ARC / CIRCULAR PROGRESS
        p.setPen(pen)
        p.drawArc(margin, margin, width, height, -90 * 16, -value * 16)

        pen.setColor(QColor(self.text_color))
        p.setPen(pen)
        p.drawText(rect, Qt.AlignCenter, f"{self.value}{self.suffix}")

        # END
        p.end()


class FileEdit(QLineEdit):
    def __init__(self, parent):
        super(FileEdit, self).__init__(parent)

        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            # for some reason, this doubles up the intro slash
            filepath = str(urls[0].path())[1:]
            self.setText(filepath)
