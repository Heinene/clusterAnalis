import math
import sys
import itertools
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QGraphicsView, QRadioButton

coord = "(20, -10);(3, 9);(36, -15);(26, 21);(12, -9);(-11, 33);(12, 8);(-30, 15);(-25, 8)"
Manhat = "(23, 7);(-4, 17);(5, 2)"
chebi = "(17, 8);(5, 1);(-12, 19)"

class qt(object):
    def __init__(self, obj):
        super().__init__()
        self.Uiset(obj)
        self.retranslateUi(obj)
        self.graphicsView = QGraphicsView(obj)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 791, 441))
        self.graphicsView.setObjectName("graphicsView")
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        pen = QtGui.QPen(QtCore.Qt.GlobalColor.gray)
        for i in range(-1 * self.graphicsView.height() // 2 + 10, self.graphicsView.height() // 2 - 10):
            r1 = QtCore.QRectF(QtCore.QPointF(0, i), QtCore.QSizeF(1, 1))
            self.scene.addRect(r1, pen)

        for i in range(-1 * self.graphicsView.width() // 2 + 10, self.graphicsView.width() // 2 - 10):
            r2 = QtCore.QRectF(QtCore.QPointF(i, 0), QtCore.QSizeF(1, 1))
            self.scene.addRect(r2, pen)

        self.coordsContainer = []
        self.centersContainer = []
        self.clastersContainer = []
        self.distance = None

    def Uiset(self, Form):
        Form.setObjectName("Form")
        Form.resize(815, 678)

        self.startPushButton = QPushButton(Form)
        self.startPushButton.clicked.connect(self.click)
        self.startPushButton.setGeometry(QtCore.QRect(260, 620, 261, 41))
        self.startPushButton.setObjectName("startPushButton")

        self.coordsTextBox = QtWidgets.QPlainTextEdit(Form)
        self.coordsTextBox.setGeometry(QtCore.QRect(260, 470, 261, 81))
        self.coordsTextBox.setObjectName("coordsTextBox")

        self.CentersTextBox = QtWidgets.QPlainTextEdit(Form)
        self.CentersTextBox.setGeometry(QtCore.QRect(540, 470, 261, 81))
        self.CentersTextBox.setObjectName("CentersTextBox")

        self.addCordsPushButton = QPushButton(Form)
        self.addCordsPushButton.clicked.connect(self.pushButt)
        self.addCordsPushButton.setGeometry(QtCore.QRect(260, 570, 541, 31))
        self.addCordsPushButton.setObjectName("addCordsPushButton")

        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 460, 241, 91))
        self.groupBox.setObjectName("groupBox")

        self.manhattanRadioButton = QRadioButton(self.groupBox)
        self.manhattanRadioButton.toggled.connect(self.manhatt)
        self.manhattanRadioButton.setGeometry(QtCore.QRect(10, 20, 221, 31))
        self.manhattanRadioButton.setObjectName("manhattanRadioButton")

        self.chebishevRadioButton = QRadioButton(self.groupBox)
        self.chebishevRadioButton.toggled.connect(self.chebi)
        self.chebishevRadioButton.setGeometry(QtCore.QRect(10, 50, 221, 41))
        self.chebishevRadioButton.setObjectName("chebishevRadioButton")

        self.stepPushButton = QPushButton(Form)
        self.stepPushButton.clicked.connect(self.stepPushButton_button_clicked)
        self.stepPushButton.setGeometry(QtCore.QRect(540, 620, 261, 41))
        self.stepPushButton.setObjectName("stepPushButton")

        self.restartPushButton = QPushButton(Form)
        self.restartPushButton.clicked.connect(self.restar)
        self.restartPushButton.setGeometry(QtCore.QRect(10, 620, 241, 41))
        self.restartPushButton.setObjectName("restartPushButton")

        self.testPushButton = QPushButton(Form)
        self.testPushButton.clicked.connect(self.testPushButton_button_clicked)
        self.testPushButton.setGeometry(QtCore.QRect(10, 570, 241, 31))
        self.testPushButton.setObjectName("testPushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.startPushButton.setText(_translate("Form", "START"))
        self.addCordsPushButton.setText(_translate("Form", "ADD COORDINATES"))
        self.groupBox.setTitle(_translate("Form", "Distance"))
        self.manhattanRadioButton.setText(_translate("Form", "Manhattan"))
        self.chebishevRadioButton.setText(_translate("Form", "Chebishev"))
        self.stepPushButton.setText(_translate("Form", "STEP"))
        self.restartPushButton.setText(_translate("Form", "RESTART"))
        self.testPushButton.setText(_translate("Form", "Set Test Dataset"))

    def LineDr(self):
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.blue)
        brush = QtGui.QBrush(QtCore.Qt.GlobalColor.blue)
        pen.setWidth(2)
        pen.setColor(QtCore.Qt.GlobalColor.blue)

        for i in range(len(self.clastersContainer)):
            for j in self.clastersContainer[i]:
                self.scene.addLine(QtCore.QLineF(4 * j[0], -4 * j[1], 4 * self.centersContainer[i][0],
                                                 -4 * self.centersContainer[i][1]), pen)

    def Pars(self, coords, centers):
        coords_l = None
        centers_l = None
        try:
            coords_string_array = coords.split(';')
            centers_string_array = centers.split(';')
            coords_l = []
            centers_l = []

            for i in coords_string_array:
                l = [float(k) for k in i.strip('()').split(',')]
                coords_l.append(l)

            for i in centers_string_array:
                l = [float(k) for k in i.strip('()').split(',')]
                centers_l.append(l)
        except:
            self.CentersTextBox.clear()
            self.coordsTextBox.clear()
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Format Error")
            msg.setInformativeText('Follow the format!')
            msg.setWindowTitle("Error")
            msg.setStyleSheet("QLabel{font-size: 20px;}")
            msg.exec_()
            pass
        return coords_l, centers_l

    def Coordin(self):
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.black)
        brush = QtGui.QBrush(QtCore.Qt.GlobalColor.black)
        side = 4
        for i in self.coordsContainer:
            self.scene.addEllipse(i[0] * side - 3, -1 * i[1] * side - 3, 7, 7, pen, brush)

        pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)
        brush = QtGui.QBrush(QtCore.Qt.GlobalColor.red)

        for i in self.centersContainer:
            self.scene.addEllipse(i[0] * side - 3, -1 * i[1] * side - 3, 7, 7, pen, brush)

    def pushButt(self):
        coordinates = self.coordsTextBox.toPlainText()
        centers = self.CentersTextBox.toPlainText()
        if coordinates == '' or centers == '':
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Data Empty")
            msg.setInformativeText('Please, enter coords')
            msg.setWindowTitle("Error")
            msg.setStyleSheet("QLabel{font-size: 20px;}")
            msg.exec_()
            return

        coordinates_l, centers_l = self.Pars(coordinates, centers)

        if coordinates_l is not None and centers_l is not None:
            co = self.coordsContainer.copy()
            ce = self.centersContainer.copy()

            co += coordinates_l.copy()
            ce += centers_l.copy()

            co.sort()
            ce.sort()

            co_new = list(num for num, _ in itertools.groupby(co))
            ce_new = list(num for num, _ in itertools.groupby(ce))

            self.centersContainer = ce_new.copy()
            self.coordsContainer = co_new.copy()

            print(self.centersContainer)
            print(self.coordsContainer)

            self.Coordin()

    def click(self):
        if self.coordsContainer == [] or self.centersContainer == []:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Data Empty")
            msg.setInformativeText('Please, enter coords')
            msg.setWindowTitle("Error")
            msg.setStyleSheet("QLabel{font-size: 20px;}")
            msg.exec_()
            return
        self.chebishevRadioButton.setEnabled(False)
        self.manhattanRadioButton.setEnabled(False)
        self.addCordsPushButton.setEnabled(False)
        self.coordsTextBox.setEnabled(False)
        self.CentersTextBox.setEnabled(False)
        self.startPushButton.setEnabled(False)
        self.testPushButton.setEnabled(False)

        if self.distance == 'M':

            for _ in range(len(self.centersContainer)):
                self.clastersContainer.append([])

            for i in self.coordsContainer:
                range_l = []
                for c in self.centersContainer:
                    range_l.append(abs(i[0] - c[0]) + abs(i[1] - c[1]))

                minindex = range_l.index(min(range_l))
                self.clastersContainer[minindex].append(i)
            self.LineDr()
        elif self.distance == 'H':
            for _ in range(len(self.centersContainer)):
                self.clastersContainer.append([])

            for i in self.coordsContainer:
                range_l = []
                for c in self.centersContainer:
                    range_l.append(max(abs(i[0] - c[0]), abs(i[1] - c[1])))

                minindex = range_l.index(min(range_l))
                self.clastersContainer[minindex].append(i)
            self.LineDr()

    def stepPushButton_button_clicked(self):
        if self.centersContainer is None or self.coordsContainer is None:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Empty Error")
            msg.setInformativeText('Not enough dots!')
            msg.setWindowTitle("Error")
            msg.setStyleSheet("QLabel{font-size: 20px;}")
            msg.exec_()
            return

        claster_backup = self.clastersContainer.copy()
        new_centers = []
        for i in self.clastersContainer:
            new_x, new_y = 0, 0
            for k in i:
                new_x += k[0]
                new_y += k[1]
            new_x /= len(i)
            new_y /= len(i)
            new_centers.append([new_x, new_y])

        self.centersContainer = new_centers.copy()
        self.redr(False)
        self.Coordin()
        self.clastersContainer.clear()
        for _ in range(len(self.centersContainer)):
            self.clastersContainer.append([])

        for i in self.coordsContainer:
            range_l = []
            for c in new_centers:
                range_l.append(math.sqrt((i[0] - c[0]) ** 2 + (i[1] - c[1]) ** 2))

            minindex = range_l.index(min(range_l))
            self.clastersContainer[minindex].append(i)
        self.LineDr()
        new_back_clasters = self.clastersContainer.copy()

        if claster_backup == new_back_clasters:
            self.stepPushButton.setEnabled(False)

    def redr(self, full):
        self.scene.clear()
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.gray)
        for i in range(-1 * self.graphicsView.height() // 2 + 10, self.graphicsView.height() // 2 - 10):
            r1 = QtCore.QRectF(QtCore.QPointF(0, i), QtCore.QSizeF(1, 1))
            self.scene.addRect(r1, pen)

        for i in range(-1 * self.graphicsView.width() // 2 + 10, self.graphicsView.width() // 2 - 10):
            r2 = QtCore.QRectF(QtCore.QPointF(i, 0), QtCore.QSizeF(1, 1))
            self.scene.addRect(r2, pen)
        if not full:

            pen2 = QtGui.QPen(QtCore.Qt.GlobalColor.black)
            brush2 = QtGui.QBrush(QtCore.Qt.GlobalColor.black)

            side = 4
            for i in self.coordsContainer:
                self.scene.addEllipse(i[0] * side - 3, -1 * i[1] * side - 3, 7, 7, pen2, brush2)

    def restar(self):
        self.chebishevRadioButton.setEnabled(True)
        self.manhattanRadioButton.setEnabled(True)
        self.addCordsPushButton.setEnabled(True)
        self.coordsTextBox.setEnabled(True)
        self.CentersTextBox.setEnabled(True)
        self.testPushButton.setEnabled(True)
        self.startPushButton.setEnabled(True)
        self.stepPushButton.setEnabled(True)
        self.redr(True)

        self.coordsContainer.clear()
        self.centersContainer.clear()
        self.clastersContainer.clear()

    def testPushButton_button_clicked(self):
        self.coordsTextBox.setPlainText(coord)
        if self.distance == 'M':
            self.CentersTextBox.setPlainText(Manhat)
        elif self.distance == 'H':
            self.CentersTextBox.setPlainText(chebi)
        else:
            self.coordsTextBox.clear()
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Distance not set")
            msg.setInformativeText('Please, pick the distance')
            msg.setWindowTitle("Error")
            msg.setStyleSheet("QLabel{font-size: 20px;}")
            msg.exec_()
            pass

    def manhatt(self):
        if self.manhattanRadioButton.isChecked():
            self.distance = 'M'

    def chebi(self):
        if self.chebishevRadioButton.isChecked():
            self.distance = 'H'


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    app2 = qt(widget)
    widget.setWindowTitle("Neural_network")
    widget.setFixedWidth(810)
    widget.setFixedHeight(670)
    widget.show()
    exit(app.exec_())


