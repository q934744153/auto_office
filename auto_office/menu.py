# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './menu.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(603, 491)
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setGeometry(QtCore.QRect(10, 100, 121, 31))
        self.toolButton.setObjectName("toolButton")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(150, 90, 421, 111))
        self.textEdit.setObjectName("textEdit")
        self.toolButton_2 = QtWidgets.QToolButton(Form)
        self.toolButton_2.setGeometry(QtCore.QRect(10, 210, 121, 31))
        self.toolButton_2.setObjectName("toolButton_2")
        self.toolButton_3 = QtWidgets.QToolButton(Form)
        self.toolButton_3.setGeometry(QtCore.QRect(20, 350, 81, 31))
        self.toolButton_3.setObjectName("toolButton_3")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(140, 330, 201, 101))
        self.textBrowser.setObjectName("textBrowser")
        self.textEdit1 = QtWidgets.QTextEdit(Form)
        self.textEdit1.setGeometry(QtCore.QRect(150, 210, 421, 91))
        self.textEdit1.setObjectName("textEdit1")
        self.toolButton_4 = QtWidgets.QToolButton(Form)
        self.toolButton_4.setGeometry(QtCore.QRect(420, 400, 131, 31))
        self.toolButton_4.setObjectName("toolButton_4")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(410, 330, 150, 46))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 420, 141, 21))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(170, 40, 231, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 191, 24))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "办公小程序-小虾米"))
        self.toolButton.setText(_translate("Form", "open file"))
        self.toolButton_2.setText(_translate("Form", "save to"))
        self.toolButton_3.setText(_translate("Form", "start"))
        self.toolButton_4.setText(_translate("Form", "map table"))
        self.pushButton.setText(_translate("Form", "使用说明"))
        self.label.setText(_translate("Form", "办公小程序：v1.1"))
        self.comboBox.setCurrentText(_translate("Form", "职能中心费用转换"))
        self.comboBox.setItemText(0, _translate("Form", "职能中心费用转换"))
        self.comboBox.setItemText(1, _translate("Form", "预提费用统计转换"))
        self.label_2.setText(_translate("Form", "请选择输出表"))

