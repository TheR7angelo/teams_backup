from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect


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