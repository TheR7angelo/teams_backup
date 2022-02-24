from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Property, QPoint, QRect
from PySide6.QtGui import Qt, QPainter, QColor
from PySide6.QtWidgets import QCheckBox


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
