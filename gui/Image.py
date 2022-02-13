from PyQt5 import QtCore, QtGui, QtWidgets
from controller import ImageProcessing


class Image(QtWidgets.QLabel):
    def __init__(self, controller: ImageProcessing, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.point = None

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        self.point = self.controller.points.check((ev.x(), ev.y()))
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if ev.buttons() == QtCore.Qt.LeftButton:
            if modifiers == QtCore.Qt.ShiftModifier:
                self.controller.take_point((ev.x(), ev.y()))
            else:
                self.controller.point_add((ev.x(), ev.y()))
        elif ev.buttons() == QtCore.Qt.RightButton:
            self.controller.point_or_line_delete((ev.x(), ev.y()))
        #self.image_update(self.controller.last_drawn_image)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        if ev.buttons() == QtCore.Qt.LeftButton:
            pass


        self.image_update(self.controller.last_drawn_image)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if ev.buttons() == QtCore.Qt.LeftButton:
            if modifiers == QtCore.Qt.ShiftModifier:
                self.controller.move_point((ev.x(), ev.y()))
        image = self.controller.mouse_over((ev.x(), ev.y()))
        if image is not None:
            self.image_update(image)

    def image_update(self, image):
        height, width, channel = image.shape
        bytes_per_line = channel * width
        image = QtGui.QImage(image, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.setPixmap(QtGui.QPixmap.fromImage(image))