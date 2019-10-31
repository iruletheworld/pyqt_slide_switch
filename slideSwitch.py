# -*- coding: utf-8 -*-

'''
Modifications for compatibility with Python 2 and better appearance.

The original C++ code was postdd by IMAN4K:
https://stackoverflow.com/a/38102598

The original Python version was ported by Stefan Scherfke:
https://stackoverflow.com/a/51825815

This version is an edit based on Stefan Scherfke's work.

The notable changes are the following.

* Set Android style as default (:code:`thumb_radius` is larger than
  :code:`track_radius`)
* Allow input colour palette
* Allow other customisations
* Explicit arguments in :code:`super()` for compatability

This version is maintained by Dr. Gāo， Sī Yǔ
'''

from PyQt5.QtCore import QPropertyAnimation, QRectF, QSize, Qt, pyqtProperty
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import (
    QAbstractButton,
    QApplication,
    QHBoxLayout,
    QSizePolicy,
    QWidget,
)

__version__ = '1.0.0'


class SlideSwitch(QAbstractButton):
    '''
    '''

    def __init__(self, parent=None,
                 track_radius=10, thumb_radius=14,
                 track_opacity=0.5,
                 color_palette=None,
                 thumb_txt_true='', thumb_txt_false='',
                 thumb_opacity=1.0, text_opacity=1.0,
                 animate_dur=120):

        super(SlideSwitch, self).__init__(parent=parent)

        self.setCheckable(True)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._track_radius = track_radius

        self._thumb_radius = thumb_radius

        self._track_opacity = track_opacity

        self._margin       = max(0, self._thumb_radius - self._track_radius)

        self._base_offset  = max(self._thumb_radius, self._track_radius)

        self._end_offset = {
            True: (lambda: self.width() - self._base_offset),
            False: (lambda: self._base_offset),
        }

        self._offset = self._base_offset

        self.thumb_opacity = thumb_opacity

        self.text_opacity = text_opacity

        self.animate_dur = animate_dur

        if color_palette:

            if isinstance(color_palette, QPalette):

                palette = self.palette()

            else:

                raise ValueError(
                    'Input argument "color_palette"'
                    + ' must be None or a QPalette object')

        else:

            palette = color_palette

        self.setPalette(palette=palette)

        self.setThumbText(text_true=thumb_txt_true, text_false=thumb_txt_false)

    def setPalette(self, palette):

        # palette = self.palette()

        if self._thumb_radius > self._track_radius:

            self._track_color = {
                True: palette.highlight(),
                False: palette.dark(),
            }

            self._thumb_color = {
                True: palette.highlight(),
                False: palette.light(),
            }

            self._text_color = {
                True: palette.highlightedText().color(),
                False: palette.dark().color(),
            }

            # self._thumb_text = {
            #     True: '',
            #     False: '',
            # }

            # self._track_opacity = 0.5

        else:

            self._thumb_color = {
                True: palette.highlightedText(),
                False: palette.light(),
            }

            self._track_color = {
                True: palette.highlight(),
                False: palette.dark(),
            }

            self._text_color = {
                True: palette.highlight().color(),
                False: palette.dark().color(),
            }

            # self._thumb_text = {
            #     True: '✔',
            #     False: '✕',
            # }

            # self._track_opacity = 1

    def setThumbText(self, text_true, text_false):
        '''
        '''

        self._thumb_text = {
                True: text_true,
                False: text_false,
            }

    @pyqtProperty(int)
    def offset(self):

        return self._offset

    @offset.setter
    def offset(self, value):

        self._offset = value

        self.update()

    def sizeHint(self):  # pylint: disable=invalid-name

        return QSize(
            4 * self._track_radius + 2 * self._margin,
            2 * self._track_radius + 2 * self._margin,
        )

    def setChecked(self, checked):

        super(SlideSwitch, self).setChecked(checked)

        self.offset = self._end_offset[checked]()

    def resizeEvent(self, event):

        super(SlideSwitch, self).resizeEvent(event)

        self.offset = self._end_offset[self.isChecked()]()

    def paintEvent(self, event):  # pylint: disable=invalid-name, unused-argument

        p = QPainter(self)

        p.setRenderHint(QPainter.Antialiasing, True)

        p.setPen(Qt.NoPen)

        track_opacity = self._track_opacity

        thumb_opacity = self.thumb_opacity

        text_opacity = self.text_opacity

        if self.isEnabled():

            track_brush = self._track_color[self.isChecked()]

            thumb_brush = self._thumb_color[self.isChecked()]

            text_color = self._text_color[self.isChecked()]

        else:

            track_opacity *= 0.8

            track_brush = self.palette().shadow()

            thumb_brush = self.palette().mid()

            text_color = self.palette().shadow().color()

        p.setBrush(track_brush)

        p.setOpacity(track_opacity)

        p.drawRoundedRect(
            self._margin,
            self._margin,
            self.width() - 2 * self._margin,
            self.height() - 2 * self._margin,
            self._track_radius,
            self._track_radius,
        )

        p.setBrush(thumb_brush)

        p.setOpacity(thumb_opacity)

        p.drawEllipse(
            self.offset - self._thumb_radius,
            self._base_offset - self._thumb_radius,
            2 * self._thumb_radius,
            2 * self._thumb_radius,
        )

        p.setPen(text_color)

        p.setOpacity(text_opacity)

        font = p.font()

        font.setPixelSize(1.5 * self._thumb_radius)

        p.setFont(font)

        p.drawText(
            QRectF(
                self.offset - self._thumb_radius,
                self._base_offset - self._thumb_radius,
                2 * self._thumb_radius,
                2 * self._thumb_radius,
            ),
            Qt.AlignCenter,
            self._thumb_text[self.isChecked()],
        )

    def mouseReleaseEvent(self, event):  # pylint: disable=invalid-name

        super(SlideSwitch, self).mouseReleaseEvent(event)

        if event.button() == Qt.LeftButton:

            anim = QPropertyAnimation(self, b'offset', self)

            anim.setDuration(self.animate_dur)
            # anim.setDuration(120)

            anim.setStartValue(self.offset)

            anim.setEndValue(self._end_offset[self.isChecked()]())

            anim.start()

    def enterEvent(self, event):  # pylint: disable=invalid-name

        self.setCursor(Qt.PointingHandCursor)

        super(SlideSwitch, self).enterEvent(event)
