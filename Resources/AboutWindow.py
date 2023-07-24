# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AboutWindowTpwSAy.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QLabel,
    QSizePolicy, QTextEdit, QWidget)

class About_Dialog(QDialog):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(640, 480)
        Dialog.setMinimumSize(QSize(640, 480))
        Dialog.setMaximumSize(QSize(640, 480))
        icon = QIcon()
        icon.addFile(u"ICONS/AppLogo.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.AVR_label = QLabel(Dialog)
        self.AVR_label.setObjectName(u"AVR_label")
        self.AVR_label.setEnabled(True)
        self.AVR_label.setGeometry(QRect(20, 52, 285, 149))
        self.AVR_label.setStyleSheet(u"")
        self.AVR_label.setPixmap(QPixmap(u"ICONS/ARC logo.png"))
        self.AVR_label.setScaledContents(True)
        self.AVR_label.setAlignment(Qt.AlignCenter)
        self.AVR_label.setWordWrap(False)
        self.AVR_label.setMargin(0)
        self.AVR_label.setIndent(0)
        self.AVR_label.setTextInteractionFlags(Qt.NoTextInteraction)
        self.textEdit = QTextEdit(Dialog)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(24, 232, 569, 237))
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setReadOnly(True)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"About", None))
        self.AVR_label.setText("")
        self.textEdit.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">AVR Programmer V1.0</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This app was created by Omar Al Rafei. It is intended for educational purposes only. Commercial use is prohibited under the following licenses:</p>\n"
"<ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-inde"
                        "nt: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Software License:</span> This app is distributed under the GNU General Public License (GPL) version 3 or later. You can find a copy of the license at <a href=\"https://www.gnu.org/licenses/gpl.html\"><span style=\" text-decoration: underline; color:#0000ff;\">gnu.org/licenses/gpl.html</span></a>.</li>\n"
"<li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Attribution:</span> You are required to give proper attribution to the author, Omar Al Rafei, whenever using or distributing this app.</li></ol></body></html>", None))
    # retranslateUi

