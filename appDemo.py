# -*- coding: utf-8 -*-

'''
'''

import os
import sys
import random
from random import randint

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette

from guiDemo import Ui_MainWindow
from slideSwitch import SlideSwitch


class AppDemo(Ui_MainWindow):

    def __init__(self):

        super(AppDemo, self).__init__()

    def setupUi(self, MW):

        super(AppDemo, self).setupUi(MW)

        self.palette_red_green = QPalette()

        self.palette_red_green.setColor(QPalette.Highlight, QColor(0, 136, 0))
        self.palette_red_green.setColor(QPalette.Shadow, QColor(128, 0, 0))

        self.slideSwitch01.setPalette(self.palette_red_green)

        self.palette_black_orange = QPalette()

        self.palette_black_orange.setColor(QPalette.Highlight, QColor(255, 140, 0))
        self.palette_black_orange.setColor(QPalette.Shadow, QColor(0, 0, 0))

        self.slideSwitch02.setPalette(self.palette_black_orange)

        self.palette_white_purple = QPalette()

        self.palette_white_purple.setColor(QPalette.Highlight, QColor(123, 104, 238))
        self.palette_white_purple.setColor(QPalette.Shadow, QColor(200, 200, 200))

        self.palette_white_purple.setColor(QPalette.HighlightedText, QColor(255, 255, 0))
        self.palette_white_purple.setColor(QPalette.Text, QColor(255, 255, 255))

        self.slideSwitch03.setPalette(self.palette_white_purple)
        self.slideSwitch03.setThumbText('On', 'Off')

        self.default_palette = self.slideSwitch04.palette()
        self.slideSwitch04.setThumbText('✔', '✕')

        self.slideSwitch01.toggled['bool'].connect(self.label01.setEnabled)
        self.slideSwitch02.toggled['bool'].connect(self.label02.setEnabled)
        self.slideSwitch03.toggled['bool'].connect(self.label03.setEnabled)
        self.slideSwitch04.toggled['bool'].connect(self.label04.setEnabled)

        self.allOn()

        self.label01.setEnabled(self.slideSwitch01.isChecked())
        self.label02.setEnabled(self.slideSwitch02.isChecked())
        self.label03.setEnabled(self.slideSwitch03.isChecked())
        self.label04.setEnabled(self.slideSwitch04.isChecked())

        self.btnDefault.clicked.connect(self.defaultColors)
        self.btnShuffle.clicked.connect(self.shuffleColors)

        self.btnAllOff.clicked.connect(self.allOff)
        self.btnAllOn.clicked.connect(self.allOn)

    def defaultColors(self):
        '''
        '''

        list_switches = [
            self.slideSwitch01,
            self.slideSwitch02,
            self.slideSwitch03,
            self.slideSwitch04
        ]

        list_palettes = [
            self.palette_red_green,
            self.palette_black_orange,
            self.palette_white_purple,
            self.default_palette
        ]

        for i, j in zip(list_switches, list_palettes):

            i.setPalette(j)

            i.update()

    def shuffleColors(self):
        '''
        '''

        list_switches = [
            self.slideSwitch01,
            self.slideSwitch02,
            self.slideSwitch03,
            self.slideSwitch04
        ]

        for i in list_switches:

            random.seed()

            palette_temp = QPalette()

            palette_temp.setColor(QPalette.Highlight, QColor(randint(0,255), randint(0,255), randint(0,255)))
            palette_temp.setColor(QPalette.Shadow, QColor(randint(0,255), randint(0,255), randint(0,255)))

            i.setPalette(palette_temp)

            i.update()

    def allOn(self):
        '''
        '''

        list_switches = [
            self.slideSwitch01,
            self.slideSwitch02,
            self.slideSwitch03,
            self.slideSwitch04
        ]

        for i in list_switches:

            i.setChecked(True)

    def allOff(self):
        '''
        '''

        list_switches = [
            self.slideSwitch01,
            self.slideSwitch02,
            self.slideSwitch03,
            self.slideSwitch04
        ]

        for i in list_switches:

            i.setChecked(False)


def main():
    '''
    This is the main entry point of the app.
    '''

    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = AppDemo()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# run app
if __name__ == '__main__':

    main()
