# -*- coding: utf-8 -*-

"""

介绍：关于图片和文字识别问题，采用Python、QT编程方法，制作出一个简单的图片文字识别软件；达到了对银行卡识别功能，实现了对识别结果进行复制功能。

主要工作：
1.UI界面的设计
2.整个程序函数的书写（功能实现）
3.软件的测试与打包

"""

# Form implementation generated from reading ui file 'imgreconition.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!
import json
import sys

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import urllib, urllib.request
import ssl

import base64


API_KEY = ''
SECRET = ''


P_KEY = ''
P_SECRET = ''


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 471)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(90, 50, 171, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")

        self.horizontalLayout.addWidget(self.comboBox)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 100, 300, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(40, 140, 271, 261))
        # self.label_3.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.label_3.setStyleSheet("border-width: 1px;border-style: solid;boder-color: rgb(0,0,0);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(330, 50, 241, 321))
        # self.label_4.setStyleSheet("background-color: rgb(85, 255, 0);")
        self.label_4.setStyleSheet("border-width: 1px;border-style: solid;boder-color: rgb(0,0,0);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 380, 241, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "AI图片识别软件"))
        self.label.setText(_translate("Form", "识别类型:"))
        self.comboBox.setItemText(0, _translate("Form", "银行卡"))
        self.label_2.setText(_translate("Form", "选择要识别的图片:"))
        self.pushButton.setText(_translate("Form", "选择"))
        self.pushButton_2.setText(_translate("Form", "复制导粘贴板"))
        # 为选择按钮添加点击事件
        self.pushButton.clicked.connect(self.openfile)
        # 为复制按钮添加点击事件
        self.pushButton_2.clicked.connect(self.copyText)

    # 复制功能函数
    def copyText(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.label_4.text())

    # 打开文件函数
    def openfile(self):
        self.download_path = QFileDialog.getOpenFileName(self.horizontalLayoutWidget_2, "选择要识别的图片", "/",
                                                         "Image File(*.jpg *.png)")
        if not self.download_path[0].strip():
            pass
        else:
            # print(self.download_path[0])
            # 把图片路径显示
            self.lineEdit.setText(self.download_path[0])
            # 显示选择的图片 自动解析图片
            pixmap = QPixmap(self.download_path[0])
            # 处理图片  规定大小
            scarePixmap = pixmap.scaled(QSize(271, 261), aspectRatioMode=Qt.KeepAspectRatio)
            # 把图片设置到控件里
            self.label_3.setPixmap(scarePixmap)
            # 通过百度ai接口来识别特定类别的图片
            self.typeTp()

    # 类别 识别
    def typeTp(self):
        # 银行卡
        if self.comboBox.currentIndex() == 0:
            # 获取token值
            self.get_bankcard(self.get_token())


    # 获取token  文字识别
    def get_token(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_KEY + '&client_secret=' + SECRET
        response = requests.get(host)
        if response:
            # print(response.json())
            self.access_token = response.json()['access_token']
            return self.access_token

    # 获取token  图像识别
    def img_get_token(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + P_KEY + '&client_secret=' + P_SECRET
        response = requests.get(host)
        if response:
            # print(response.json())
            self.access_token = response.json()['access_token']
            return self.access_token



    # 银行卡识别函数
    def get_bankcard(self, access_token):
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/bankcard"
        # 二进制方式打开图片文件
        f = open(self.download_path[0], 'rb')
        img = base64.b64encode(f.read())
        params = {"image": img}
        # params = urllib.parse.urlencode(params).encode('utf-8')
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            # 解析返回的数据
            rs = response.json()
            # print(response.json())
            # 读取数据
            strover = '识别结果：\n'
            try:
                if rs['result']['bank_card_type'] == 0:
                    bank_card_type = '不能识别'
                elif rs['result']['bank_card_type'] == 1:
                    bank_card_type = '借记卡'
                elif rs['result']['bank_card_type'] == 2:
                    bank_card_type = '信用卡'
                strover += '卡号：   {}'.format(rs['result']['bank_card_number'])
            except Exception:
                strover += '解析错误'
            # 把结果显示到控件
            self.label_4.setText(strover)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
