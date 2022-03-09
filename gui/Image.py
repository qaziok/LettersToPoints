from PyQt5 import QtCore, QtGui, QtWidgets
from controller import ImageProcessing


class Image(QtWidgets.QLabel):
    def __init__(self, controller: ImageProcessing, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.point = None

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        # lewy
        if ev.buttons() == QtCore.Qt.LeftButton:
            self.controller.move_point((ev.x(), ev.y()))

        image = self.controller.mouse_over((ev.x(), ev.y()))
        if image is not None:
            self.image_update(image)

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        self.point = self.controller.points.check((ev.x(), ev.y()))
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        coords = (ev.x(), ev.y())
        self.press_location = coords

        # lewy
        if ev.buttons() == QtCore.Qt.LeftButton:

            if modifiers == QtCore.Qt.ShiftModifier:
                pass
            elif modifiers == QtCore.Qt.ControlModifier:
                self.controller.point_add(coords)
                self.controller.add_to_buffer(coords)
            elif modifiers == QtCore.Qt.AltModifier:
                pass
            elif modifiers == QtCore.Qt.NoModifier:
                self.controller.take_point(coords)


        # prawy
        elif ev.buttons() == QtCore.Qt.RightButton:

            if modifiers == QtCore.Qt.ShiftModifier:
                pass
            elif modifiers == QtCore.Qt.ControlModifier:
                self.controller.delete_from_buffer(coords)
            elif modifiers == QtCore.Qt.NoModifier:
                if self.controller.point_delete(coords):
                    pass
                elif self.controller.line_delete(coords):
                    pass

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        coords = (ev.x(), ev.y())
        if ev.button() == QtCore.Qt.LeftButton:
            if (coords[0]-self.press_location[0])**2 + (coords[1]-self.press_location[1]) <= 10:
                self.controller.point_add(coords)
            self.controller.taken_point = None
        self.image_update(self.controller.last_drawn_image)

    def image_update(self, image):
        height, width, channel = image.shape
        bytes_per_line = channel * width
        image = QtGui.QImage(image, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.setPixmap(QtGui.QPixmap.fromImage(image))