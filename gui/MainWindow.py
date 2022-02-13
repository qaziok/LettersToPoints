from PyQt5 import QtCore, QtGui, QtWidgets
from gui.Image import Image
from controller import ImageProcessing


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 870)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        distance = 20
        self.lab_label = QtWidgets.QLabel(self.centralwidget)
        self.lab_label.setGeometry(QtCore.QRect(30, distance, 211, 20))
        self.lab_label.setObjectName("lab_label")
        distance += 20
        self.lab = QtWidgets.QComboBox(self.centralwidget)
        self.lab.setGeometry(QtCore.QRect(20, distance, 230, 30))
        self.lab.setObjectName("lab")
        self.lab.addItem("")
        self.lab.addItem("")
        self.lab.addItem("")
        self.lab.addItem("")
        self.lab.addItem("")
        distance += 30 + 10
        self.mode_label = QtWidgets.QLabel(self.centralwidget)
        self.mode_label.setGeometry(QtCore.QRect(30, distance, 211, 20))
        self.mode_label.setObjectName("mode_label")
        distance += 20
        self.mode = QtWidgets.QComboBox(self.centralwidget)
        self.mode.setGeometry(QtCore.QRect(20, distance, 230, 30))
        self.mode.setObjectName("mode")
        self.mode.addItem("")
        self.mode.addItem("")
        self.mode.addItem("")
        self.mode.addItem("")
        self.mode.currentIndexChanged.connect(self.lock_unlock_sign)
        distance += 30 + 10
        self.sign_label = QtWidgets.QLabel(self.centralwidget)
        self.sign_label.setGeometry(QtCore.QRect(30, distance, 211, 20))
        self.sign_label.setObjectName("sign_label")
        distance += 20
        self.sign = QtWidgets.QLineEdit(self.centralwidget)
        self.sign.setGeometry(QtCore.QRect(20, distance, 230, 30))
        self.sign.setObjectName("sign")
        self.sign.setDisabled(True)
        distance += 30 + 20
        self.generate_check = QtWidgets.QCheckBox(self.centralwidget)
        self.generate_check.setGeometry(QtCore.QRect(30, distance, 210, 30))
        self.generate_check.setObjectName("generate_check")
        self.generate_check.stateChanged.connect(self.lock_unlock_generate_button)
        distance += 30
        self.generate_button = QtWidgets.QPushButton(self.centralwidget)
        self.generate_button.setGeometry(QtCore.QRect(20, distance, 230, 30))
        self.generate_button.setObjectName("generate_button")
        self.generate_button.clicked.connect(self.generate_image)
        self.generate_button.setDisabled(True)
        distance += 30 + 40
        self.scale_label = QtWidgets.QLabel(self.centralwidget)
        self.scale_label.setGeometry(QtCore.QRect(30, distance, 211, 20))
        self.scale_label.setObjectName("scale_label")
        distance += 20
        self.scale = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.scale.setGeometry(QtCore.QRect(20, distance, 230, 30))
        self.scale.setRange(0.01, 100)
        self.scale.setSingleStep(0.1)
        self.scale.setObjectName("scale")
        self.scale.setValue(1.0)
        distance += 30 + 10
        self.center_label = QtWidgets.QLabel(self.centralwidget)
        self.center_label.setGeometry(QtCore.QRect(30, distance, 211, 20))
        self.center_label.setObjectName("center_label")
        distance += 20
        self.center_x = QtWidgets.QCheckBox(self.centralwidget)
        self.center_x.setGeometry(QtCore.QRect(70, distance, 70, 30))
        self.center_x.setObjectName("center_x")
        self.center_y = QtWidgets.QCheckBox(self.centralwidget)
        self.center_y.setGeometry(QtCore.QRect(160, distance, 70, 30))
        self.center_y.setObjectName("center_y")
        distance += 30 + 10
        self.shift_label = QtWidgets.QLabel(self.centralwidget)
        self.shift_label.setGeometry(QtCore.QRect(30, distance, 211, 20))
        self.shift_label.setObjectName("shift_label")
        distance += 20
        self.shiftX_label = QtWidgets.QLabel(self.centralwidget)
        self.shiftX_label.setGeometry(QtCore.QRect(68, distance+2, 50, 20))
        self.shiftX_label.setObjectName("shiftX_label")
        self.shiftY_label = QtWidgets.QLabel(self.centralwidget)
        self.shiftY_label.setGeometry(QtCore.QRect(168, distance+2, 50, 20))
        self.shiftY_label.setObjectName("shiftY_label")
        distance += 20
        self.shiftX_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.shiftX_box.setGeometry(QtCore.QRect(40, distance, 90, 30))
        self.shiftX_box.setObjectName("shiftX_box")
        self.shiftX_box.setRange(-1000, 1000)
        self.shiftX_box.setSingleStep(1)
        self.shiftY_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.shiftY_box.setGeometry(QtCore.QRect(140, distance, 90, 30))
        self.shiftY_box.setObjectName("shiftY_box")
        self.shiftY_box.setRange(-1000, 1000)
        self.shiftY_box.setSingleStep(1)
        distance += 30 + 10
        self.type_label = QtWidgets.QLabel(self.centralwidget)
        self.type_label.setGeometry(QtCore.QRect(30, distance, 211, 20))
        self.type_label.setObjectName("type_label")
        distance += 20
        self.type_float = QtWidgets.QRadioButton(self.centralwidget)
        self.type_float.setGeometry(QtCore.QRect(160, distance, 70, 30))
        self.type_float.toggled.connect(self.type_change(float))
        self.type_float.setObjectName("type_float")

        self.type_int = QtWidgets.QRadioButton(self.centralwidget)
        self.type_int.setGeometry(QtCore.QRect(70, distance, 70, 30))
        self.type_int.toggled.connect(self.type_change(int))
        self.type_int.setChecked(True)
        self.type_int.setObjectName("type_int")
        self.data_type = int
        distance += 30 + 10
        self.points_button = QtWidgets.QPushButton(self.centralwidget)
        self.points_button.setGeometry(QtCore.QRect(20, distance, 230, 30))
        self.points_button.setObjectName("points_button")
        self.points_button.clicked.connect(self.print_output)
        distance += 30
        self.output = QtWidgets.QTextEdit(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(20, distance, 230, 180))
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        distance += 180
        self.clipboard_button = QtWidgets.QPushButton(self.centralwidget)
        self.clipboard_button.setGeometry(QtCore.QRect(20, distance, 230, 30))
        self.clipboard_button.setObjectName("clipboard_button")
        self.clipboard_button.clicked.connect(self.copy_to_clipboard)

        self.controller = ImageProcessing()
        self.controller.generate_sign('')
        self.image_preview = Image(self.controller, parent=self.centralwidget)
        self.image_preview.setMouseTracking(True)
        self.image_preview.setGeometry(QtCore.QRect(270, 20, 800, 800))
        self.image_preview.setObjectName("image_preview")
        self.image_preview.image_update(self.controller.last_drawn_image)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1091, 21))
        self.menubar.setObjectName("menubar")

        self.menuPomoc = QtWidgets.QMenu(self.menubar)
        self.menuPomoc.setObjectName("menuPomoc")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuPomoc.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Walić laborki z grafiki"))
        self.mode.setItemText(0, _translate("MainWindow", "Pusty"))
        self.mode.setItemText(1, _translate("MainWindow", "Litera bez punktów"))
        self.mode.setItemText(2, _translate("MainWindow", "Litera z punktami"))
        self.mode.setItemText(3, _translate("MainWindow", "Litera z punktami i liniami"))
        self.lab.setItemText(0, _translate("MainWindow", "Desmos"))
        self.lab.setItemText(1, _translate("MainWindow", "Xlib"))
        self.lab.setItemText(2, _translate("MainWindow", "GDI"))
        self.lab.setItemText(3, _translate("MainWindow", "DirectX"))
        self.lab.setItemText(4, _translate("MainWindow", "OpenGL"))
        self.mode_label.setText(_translate("MainWindow", "Tryb"))
        self.lab_label.setText(_translate("MainWindow", "Laboratorium"))
        self.sign_label.setText(_translate("MainWindow", "Znak"))
        self.generate_button.setText(_translate("MainWindow", "Generuj obraz"))
        self.generate_check.setText(_translate("MainWindow", "Jestem pewien!"))
        self.points_button.setText(_translate("MainWindow", "Punkty"))
        self.scale_label.setText(_translate("MainWindow", "Skala"))
        self.center_x.setText(_translate("MainWindow", "Oś X"))
        self.center_y.setText(_translate("MainWindow", "Oś Y"))
        self.center_label.setText(_translate("MainWindow", "Centrowanie"))
        self.type_label.setText(_translate("MainWindow", "Typ danych"))
        self.type_float.setText(_translate("MainWindow", "Float"))
        self.type_int.setText(_translate("MainWindow", "Int"))
        self.shift_label.setText(_translate("MainWindow", "Przesunięcie"))
        self.shiftX_label.setText(_translate("MainWindow", "Oś X"))
        self.shiftY_label.setText(_translate("MainWindow", "Oś Y"))
        self.clipboard_button.setText(_translate("MainWindow", "Skopiuj do schowka"))
        self.menuPomoc.setTitle(_translate("MainWindow", "Pomoc"))

    def print_output(self):
        option = self.lab.currentIndex()
        center_check = (self.center_x.isChecked(),self.center_y.isChecked())
        shift_check = (self.shiftX_box.value(),self.shiftY_box.value())
        self.output.setText(
            self.controller.output(
                option, self.data_type, center_check, shift_check, self.scale.value()
            )
        )

    def generate_image(self):
        self.generate_check.setChecked(False)
        letter = self.sign.text()
        self.controller.clear()
        if self.mode.currentIndex():
            self.controller.generate_sign(letter, mode=self.mode.currentIndex())
        else:
            self.controller.generate_sign('',mode=0)
        self.image_preview.image_update(self.controller.last_drawn_image)

    def lock_unlock_generate_button(self):
        if self.generate_check.isChecked():
            self.generate_button.setDisabled(False)
        else:
            self.generate_button.setDisabled(True)

    def type_change(self, type):
        return lambda: setattr(self, 'data_type', type)

    def lock_unlock_sign(self):
        if self.mode.currentIndex() == 0:
            self.sign.setDisabled(True)
        else:
            self.sign.setDisabled(False)

    def copy_to_clipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(self.output.toPlainText(),mode=clipboard.Clipboard)
