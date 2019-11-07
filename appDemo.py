# -*- coding: utf-8 -*-

'''
'''

import sys
import random
from random import randint

from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette

from guiDemo import Ui_MainWindow


class AppDemo(Ui_MainWindow):

    def __init__(self):

        super(AppDemo, self).__init__()

    def setupUi(self, MW):

        super(AppDemo, self).setupUi(MW)

        self.palette01 = QPalette()
        self.palette01.setColor(QPalette.Highlight, QColor(0, 136, 0))
        self.palette01.setColor(QPalette.Shadow, QColor(128, 0, 0))

        self.palette02 = QPalette()
        self.palette02.setColor(QPalette.Highlight, QColor(239, 120, 55))
        self.palette02.setColor(QPalette.Shadow, QColor(53, 53, 53))

        self.palette03 = QPalette()
        self.palette03.setColor(QPalette.Highlight, QColor(133, 104, 238))
        self.palette03.setColor(QPalette.Shadow, QColor(200, 200, 200))
        self.palette03.setColor(QPalette.HighlightedText, QColor(255, 255, 0))
        self.palette03.setColor(QPalette.Text, QColor(255, 255, 255))

        self.palette04 = QPalette()
        self.palette04.setColor(QPalette.Highlight, QColor(0, 0, 255))
        self.palette04.setColor(QPalette.Shadow, QColor(188, 160, 199))

        self.slideSwitch01.setPalette(self.palette01)
        self.slideSwitch02.setPalette(self.palette02)
        self.slideSwitch03.setPalette(self.palette03)
        self.slideSwitch03.setThumbText('On', 'Off')
        self.slideSwitch04.setPalette(self.palette04)
        self.slideSwitch04.setThumbText('✔', '✕')

        self.default_palette = self.slideSwitch05.palette()

        int_anim_dur = 120

        for i in range(0, 8):

            str_obj_slide_switch = 'slideSwitch'

            str_obj_lbl = 'label'

            str_no = str(i+1).zfill(2)

            str_obj_slide_switch += str_no

            obj_slide_switch = getattr(self, str_obj_slide_switch)

            if (i+1) <= 4:

                str_obj_lbl += str_no

                obj_lbl = getattr(self, str_obj_lbl)

                obj_slide_switch.toggled['bool'].connect(obj_lbl.setEnabled)

                obj_lbl.setEnabled(obj_slide_switch.isChecked())

            else:

                pass

            if (i+1) >= 5:

                int_anim_dur += int_anim_dur

                obj_slide_switch.setDirection('v')

                obj_slide_switch.setThumbText('是', '否')

                obj_slide_switch.setTrackRadius(8)

                obj_slide_switch.setAnimDur(int_anim_dur)

                font = QtGui.QFont()
                font.setFamily("Microsoft YaHei")
                font.setPointSize(6)
                obj_slide_switch.setFont(font)

                obj_slide_switch.update()

            else:

                pass

        self.allOn()

        self.btnDefault.clicked.connect(self.defaultColors)
        self.btnShuffle.clicked.connect(self.shuffleColors)

        self.btnAllOff.clicked.connect(self.allOff)
        self.btnAllOn.clicked.connect(self.allOn)

    def defaultColors(self):
        '''
        '''

        for i in range(0, 8):

            str_no = str(i+1).zfill(2)

            str_obj_slide_switch = 'slideSwitch'

            str_obj_palette = 'palette'

            str_obj_slide_switch += str_no

            str_obj_palette += str_no

            obj_slide_switch = getattr(self, str_obj_slide_switch)

            if (i+1) <= 4:

                obj_palette = getattr(self, str_obj_palette)

                obj_slide_switch.setPalette(obj_palette)

                obj_slide_switch.update()

            else:

                obj_slide_switch.setPalette(self.default_palette)

                obj_slide_switch.update()

    def shuffleColors(self):
        '''
        '''

        for i in range(0, 8):

            str_obj = 'slideSwitch'

            str_no = str(i+1).zfill(2)

            str_obj += str_no

            obj = getattr(self, str_obj)

            random.seed()

            palette_temp = QPalette()

            int_rh = randint(0, 255)
            int_gh = randint(0, 255)
            int_bh = randint(0, 255)

            int_rs = randint(0, 255)
            int_gs = randint(0, 255)
            int_bs = randint(0, 255)

            palette_temp.setColor(QPalette.Highlight,
                                  QColor(int_rh, int_gh, int_bh))
            palette_temp.setColor(
                QPalette.Shadow, QColor(int_rs, int_gs, int_bs))

            obj.setPalette(palette_temp)

            obj.update()

    def allOn(self):
        '''
        '''

        for i in range(0, 8):

            str_obj = 'slideSwitch'

            str_no = str(i+1).zfill(2)

            str_obj += str_no

            obj = getattr(self, str_obj)

            obj.setChecked(True)

    def allOff(self):
        '''
        '''

        for i in range(0, 8):

            str_obj = 'slideSwitch'

            str_no = str(i+1).zfill(2)

            str_obj += str_no

            obj = getattr(self, str_obj)

            obj.setChecked(False)


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
