from controller import ImageProcessing

from PyQt5 import QtGui, QtCore, QtWidgets
import cv2
import sys
import numpy

class Image(QtWidgets.QLabel):
    def __init__(self, controller: ImageProcessing):
        super().__init__()
        self.controller = controller
        self.controller.last_point = None

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        if ev.buttons() == QtCore.Qt.LeftButton:
            print('dodaj')
            self.controller.point_add((ev.x(), ev.y()))
        elif ev.buttons() == QtCore.Qt.RightButton:
            print('usuń')
            self.controller.point_or_line_delete((ev.x(), ev.y()))
        self.image_update(self.controller.last_drawn_image)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
        print(ev.x(), ev.y())
        image = self.controller.mouse_over((ev.x(), ev.y()))
        if image is not None:
            self.image_update(image)

    def image_update(self, image):
        height, width, channel = image.shape
        bytes_per_line = channel * width
        image = QtGui.QImage(image, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.setPixmap(QtGui.QPixmap.fromImage(image))



class DisplayImageWidget(QtWidgets.QWidget):
    def __init__(self, cont: ImageProcessing, parent=None):
        super(DisplayImageWidget, self).__init__(parent)

        self.image = cont.last_drawn_image

        self.button = QtWidgets.QPushButton('Show picture')
        self.button.clicked.connect(self.show_image)
        self.image_frame = Image(cont)
        self.image_frame.setMouseTracking(True)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.image_frame)
        self.setLayout(self.layout)

    @QtCore.pyqtSlot()
    def show_image(self):
        height, width, channel = self.image.shape
        bytes_per_line = channel * width
        image = QtGui.QImage(self.image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(image))

if __name__ == '__main__':
    image = ImageProcessing()
    image.generate_sign('Q')
    image.draw_and_update(image.rgb_image)
    #image.loop()
    app = QtWidgets.QApplication(sys.argv)
    display_image_widget = DisplayImageWidget(image)
    display_image_widget.show()
    sys.exit(app.exec_())

