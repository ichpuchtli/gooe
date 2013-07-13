gooe
====
A simple wav file manipulation program. Effects can be added to Wav files then saved to local USB drives.

#####Effects include:
* Volume
* Echo
* Delay
* Decimator ( Quantization in Frequency Domain )
* Bit Crusher ( Quantization in Amplitude Domain )
* Pitch Shift

###Requirements
* Python 2.x (http://python.org/download)
* PySide (http://pyside.org)
* numpy (http://numpy.org)
* scikits-samplerate (https://pypi.python.org/pypi/scikits.samplerate)
* setuptools (https://pypi.python.org/pypi/setuptools)

Optional:
 * winsound (http://docs.python.org/2/library/winsound.html)

### Installation
####Arch Linux
    $ pacaur -S python2 python2-distrubte python2-numpy python2-pyside
    $ wget scikits-samplerate
    $ tar -xvf scikits-samplerate.tar.gz
    $ sudo python2 setup.py
    $ python2 gooe.py

####Windows
See http://www.lfd.uci.edu/~gohlke/pythonlibs/ for the required libraies.

###Notes
Playing effected sounds in real time is only available on windows, see winsound. It should be noted
this software was a complete hack developed as part of team project for college. It was my first experience with Qt's Signal/Slot mechanism and my first time using PyQt4/PySide.

###Screenshot
![Screenshot](http://i.imgur.com/QYFESyv.png)
