# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_beam.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget_beam(object):
    def setupUi(self, widget_beam):
        widget_beam.setObjectName("widget_beam")
        widget_beam.resize(310, 497)
        widget_beam.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout = QtWidgets.QVBoxLayout(widget_beam)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frmMasterSlave = QtWidgets.QFrame(widget_beam)
        self.frmMasterSlave.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frmMasterSlave.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frmMasterSlave.setObjectName("frmMasterSlave")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frmMasterSlave)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_9 = QtWidgets.QLabel(self.frmMasterSlave)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(80, 0))
        self.label_9.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)
        self.cbMasterAxis = QtWidgets.QComboBox(self.frmMasterSlave)
        self.cbMasterAxis.setObjectName("cbMasterAxis")
        self.gridLayout_2.addWidget(self.cbMasterAxis, 0, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frmMasterSlave)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(60, 0))
        self.label_10.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 0, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frmMasterSlave)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QtCore.QSize(80, 0))
        self.label_11.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 1, 0, 1, 1)
        self.cbSlaveAxis = QtWidgets.QComboBox(self.frmMasterSlave)
        self.cbSlaveAxis.setObjectName("cbSlaveAxis")
        self.gridLayout_2.addWidget(self.cbSlaveAxis, 1, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frmMasterSlave)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QtCore.QSize(60, 0))
        self.label_12.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.frmMasterSlave)
        self.label_7 = QtWidgets.QLabel(widget_beam)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.frame = QtWidgets.QFrame(widget_beam)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.doubleSpinBox_1 = QtWidgets.QDoubleSpinBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_1.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_1.setSizePolicy(sizePolicy)
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-999999999999.0)
        self.doubleSpinBox_1.setMaximum(99999999999999.0)
        self.doubleSpinBox_1.setObjectName("doubleSpinBox_1")
        self.gridLayout.addWidget(self.doubleSpinBox_1, 0, 1, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_3.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_3.setSizePolicy(sizePolicy)
        self.doubleSpinBox_3.setDecimals(0)
        self.doubleSpinBox_3.setMinimum(-999999999999.0)
        self.doubleSpinBox_3.setMaximum(99999999999999.0)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.gridLayout.addWidget(self.doubleSpinBox_3, 2, 1, 1, 2)
        self.doubleSpinBox_5 = QtWidgets.QDoubleSpinBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_5.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_5.setSizePolicy(sizePolicy)
        self.doubleSpinBox_5.setDecimals(0)
        self.doubleSpinBox_5.setMinimum(-999999999999.0)
        self.doubleSpinBox_5.setMaximum(99999999999999.0)
        self.doubleSpinBox_5.setObjectName("doubleSpinBox_5")
        self.gridLayout.addWidget(self.doubleSpinBox_5, 4, 1, 1, 2)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy)
        self.doubleSpinBox_2.setDecimals(0)
        self.doubleSpinBox_2.setMinimum(-999999999999.0)
        self.doubleSpinBox_2.setMaximum(99999999999999.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.gridLayout.addWidget(self.doubleSpinBox_2, 1, 1, 1, 2)
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_4.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_4.setSizePolicy(sizePolicy)
        self.doubleSpinBox_4.setDecimals(0)
        self.doubleSpinBox_4.setMinimum(-999999999999.0)
        self.doubleSpinBox_4.setMaximum(99999999999999.0)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox_4")
        self.gridLayout.addWidget(self.doubleSpinBox_4, 3, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 3, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 1, 3, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 2, 3, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.frame)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 3, 3, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 4, 3, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.label_8 = QtWidgets.QLabel(widget_beam)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(widget_beam)
        QtCore.QMetaObject.connectSlotsByName(widget_beam)
        widget_beam.setTabOrder(self.cbMasterAxis, self.cbSlaveAxis)
        widget_beam.setTabOrder(self.cbSlaveAxis, self.doubleSpinBox_1)
        widget_beam.setTabOrder(self.doubleSpinBox_1, self.doubleSpinBox_2)
        widget_beam.setTabOrder(self.doubleSpinBox_2, self.doubleSpinBox_3)
        widget_beam.setTabOrder(self.doubleSpinBox_3, self.doubleSpinBox_4)
        widget_beam.setTabOrder(self.doubleSpinBox_4, self.doubleSpinBox_5)

    def retranslateUi(self, widget_beam):
        _translate = QtCore.QCoreApplication.translate
        widget_beam.setWindowTitle(_translate("widget_beam", "Form"))
        self.label_9.setText(_translate("widget_beam", "Left connection"))
        self.label_10.setText(_translate("widget_beam", "[axis]"))
        self.label_11.setText(_translate("widget_beam", "Right connection"))
        self.label_12.setText(_translate("widget_beam", "[axis]"))
        self.label_7.setText(_translate("widget_beam", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Properties</span></p></body></html>"))
        self.label_3.setText(_translate("widget_beam", "EIz"))
        self.label.setText(_translate("widget_beam", "Length"))
        self.label_2.setText(_translate("widget_beam", "EIy"))
        self.label_5.setText(_translate("widget_beam", "EA"))
        self.label_4.setText(_translate("widget_beam", "GIp"))
        self.label_6.setText(_translate("widget_beam", "[m]"))
        self.label_13.setText(_translate("widget_beam", "[kN*m2]"))
        self.label_14.setText(_translate("widget_beam", "[kN*m2]"))
        self.label_15.setText(_translate("widget_beam", "[kN*m2]"))
        self.label_16.setText(_translate("widget_beam", "[kN]"))
        self.label_8.setText(_translate("widget_beam", "<html><head/><body><p>E(steel) is ~200 GPa = 200*10^6 kN/m2</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_beam = QtWidgets.QWidget()
    ui = Ui_widget_beam()
    ui.setupUi(widget_beam)
    widget_beam.show()
    sys.exit(app.exec_())
