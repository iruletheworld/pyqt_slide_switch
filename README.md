# Android style slide switch for PyQt
A Android style slide switch in pyqt5.

Found myself one day wanting a switch like Android's while doing a GUI in pyqt5. Found a usable one, but much could be imporved. Thus this project.

The original C++ code was posted by IMAN4K:
https://stackoverflow.com/a/38102598

The original Python version was ported by Stefan Scherfke:
https://stackoverflow.com/a/51825815

The following GIF is a demo from the `appDemo.py`

<img src="./record01.gif" alt="Screen record" width="400">

Main changes include, but are not limited to, the following.

* Remove auto style change base on the values of track radius and thumb
  radius. Leave the decision to the user.

* Softcode track opacity and thumb opacity.

* Allow user defined colour palette.

* Allow thumb text settings.

* Allow thumb font size gain setting.

* Allow slide animation setting.

* Allow vertical direction.

* Always center the thumb in relation to the track.
