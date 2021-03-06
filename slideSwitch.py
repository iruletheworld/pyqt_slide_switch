# -*- coding: utf-8 -*-

'''
Modifications for compatibility with Python 2 and better appearance.
The original C++ code was posted by IMAN4K:
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
    Android style slide switch class. Inherited from :code:`QAbstractButton`.
    '''

    def __init__(self, parent=None,
                 track_radius=10, thumb_radius=18,
                 track_opacity=0.5,
                 thumb_opacity=1.0, text_opacity=1.0,
                 color_palette=None,
                 thumb_txt_true='', thumb_txt_false='',
                 animate_dur=120, font_size_gain=1.0,
                 direction='h'):
        '''
        Constructor of the SlideSwitch object.

        Parameters
        -----------
        parent : QObject

            The parent object for the slide switch

            Default = None

        track_radius : float

            Radius of the track. Affects how wide the track is and how
            "rounded" the track ends.

            Default = 10

        thumb_radius : float

            Radius of the thumb. Affects the size of the thumb circle.

            Default = 18

        track_opacity : float

            Affects the opacity of the track. Should be different than
            the opacity of thumb to make it more visible.

            Default = 0.5

        thumb_opacity : float

            Affects the opacity of the track. Should be different than
            the opacity of track to make it more visible.

            Default = 1.0

        text_opacity : float

            Affects the opacity of the texts in the thumb.

            Default = 1.0

        color_palette : QPalette

            The colour palette for the slide switch object.

            The :code:`highlight` of palette is used for the on status
            for both the track and the thumb (so they should have different)
            opacity.

            The :code:`shadow` of palette is used for the off status
            for both the track and the thumb (so they should have different)
            opacity.

            The colour of the :code:`highlightedText` of palette is
            used for the on status for the thumb text.

            The colour of the :code:`text` of palette is used for the
            off status for the thumb text.

            If a palette is not given, the inherited palette would be used.

            Default = None, i.e., the inherited palette is used.

        thumb_txt_true : string

            Text in the thumb for the on status.

            Default = ''

        thumb_txt_false : string

            Text in the thumb for the off status.

            Default = ''

        animate_dur : float

            Time duration of the animation. Affects how fast the thumb travels
            on the track.

            Default = 120

        font_size_gain : float

            Gain for the text size inside the thumb.

            Default = 1.0

        direction : string

            This must either be "h" or "v".

            "h" for horizontal switch direction.

            "v" for vertical switch direction.

            Default = 'h'
        '''

        super(SlideSwitch, self).__init__(parent=parent)

        self.setCheckable(True)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._track_radius = track_radius

        self._thumb_radius = thumb_radius

        self._margin       = max(0, self._thumb_radius - self._track_radius)

        self._base_offset  = max(self._thumb_radius, self._track_radius)

        self._offset = self._base_offset

        self.thumb_opacity = thumb_opacity

        self.text_opacity = text_opacity

        self._track_opacity = track_opacity

        self.animate_dur = animate_dur

        self.font_size_gain = font_size_gain

        if color_palette:

            if isinstance(color_palette, QPalette):

                palette = color_palette

            else:

                raise ValueError(
                    'Input argument "color_palette"'
                    + ' must be None or a QPalette object')

        else:

            palette = self.palette()

        self._track_color = None
        self._thumb_color = None
        self._text_color = None

        self.setPalette(palette=palette)

        self._thumb_text = None

        self.setThumbText(text_true=thumb_txt_true, text_false=thumb_txt_false)

        self.direction = direction.lower()

        if not (self.direction.lower() == 'h' or self.direction.lower() == 'v'):

            self.direction = 'h'

        else:

            pass

        if self.direction == 'h':

            self._end_offset = {
                True: (lambda: self.width() - self._base_offset),
                False: (lambda: self._base_offset),
            }

        else:

            self._end_offset = {
                True: (lambda: self._base_offset),
                False: (lambda: self.height() - self._base_offset),
            }

    def setTrackRadius(self, track_radius):
        '''
        '''

        self._track_radius = track_radius

    def setThumbRadius(self, thumb_radius):
        '''
        '''

        self._thumb_radius = thumb_radius

    def setFontSizeGain(self, font_size_gain):
        '''
        '''

        self.font_size_gain = font_size_gain

    def setTrackOpacity(self, track_opacity):
        '''
        '''

        self._track_opacity = track_opacity

    def setThumbText(self, text_true, text_false):
        '''
        '''

        self._thumb_text = {
                True: text_true,
                False: text_false,
            }

    def setPalette(self, palette):
        '''
        '''

        self._track_color = {
            True: palette.highlight(),
            False: palette.shadow(),
        }

        self._thumb_color = {
            True: palette.highlight(),
            False: palette.shadow(),
        }

        self._text_color = {
            True: palette.highlightedText().color(),
            False: palette.text().color(),
        }

    def setDirection(self, direction):

        self.direction = direction.lower()

        if not (self.direction.lower() == 'h' or self.direction.lower() == 'v'):

            self.direction = 'h'

        else:

            pass

        if self.direction == 'h':

            # 终点位置
            self._end_offset = {
                True: (lambda: self.width() - self._base_offset),
                False: (lambda: self._base_offset),
            }

        else:

            self._end_offset = {
                True: (lambda: self._base_offset),
                False: (lambda: self.height() - self._base_offset),
            }

    def setAnimDur(self, animate_dur):
        '''
        '''

        self.animate_dur = animate_dur

    @pyqtProperty(int)
    def offset(self):

        return self._offset

    @offset.setter
    def offset(self, value):

        self._offset = value

        self.update()

    def sizeHint(self):

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

    def paintEvent(self, event):

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

        if self.direction.lower() == 'v':

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
                self.width()/2.0 - self._thumb_radius,
                self.offset - self._thumb_radius,
                2 * self._thumb_radius,
                2 * self._thumb_radius,
            )

            p.setPen(text_color)

            p.setOpacity(text_opacity)

            font = p.font()

            font.setPixelSize(self.font_size_gain * self._thumb_radius)

            p.setFont(font)

            p.drawText(
                QRectF(
                    self.width()/2.0 - self._thumb_radius,
                    self.offset - self._thumb_radius,
                    2 * self._thumb_radius,
                    2 * self._thumb_radius,
                ),
                Qt.AlignCenter,
                self._thumb_text[self.isChecked()],
            )

        else:

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
                self.height()/2.0 - self._thumb_radius,
                2 * self._thumb_radius,
                2 * self._thumb_radius,
            )

            p.setPen(text_color)

            p.setOpacity(text_opacity)

            font = p.font()

            font.setPixelSize(self.font_size_gain * self._thumb_radius)

            p.setFont(font)

            p.drawText(
                QRectF(
                    self.offset - self._thumb_radius,
                    self.height()/2.0 - self._thumb_radius,
                    2 * self._thumb_radius,
                    2 * self._thumb_radius,
                ),
                Qt.AlignCenter,
                self._thumb_text[self.isChecked()],
            )

    def mouseReleaseEvent(self, event):

        super(SlideSwitch, self).mouseReleaseEvent(event)

        if event.button() == Qt.LeftButton:

            anim = QPropertyAnimation(self, b'offset', self)

            anim.setDuration(self.animate_dur)
            # anim.setDuration(120)

            anim.setStartValue(self.offset)

            anim.setEndValue(self._end_offset[self.isChecked()]())

            anim.start()

    def enterEvent(self, event):

        self.setCursor(Qt.PointingHandCursor)

        super(SlideSwitch, self).enterEvent(event)
