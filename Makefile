
# Resolve python paths, MINGW comes with git-windows/git-bash
ifeq (${shell uname}, MINGW32_NT-6.1)
    PYTHON=C:/python27/python.exe
else
    PYTHON=python
endif

all: gooe

gooe : gooe.py
	$(PYTHON) gooe.py

git:
	git add *
	git commit
	git push

#TODO Maybe include an install directive to setup dependencies
install:
	#wget python27
	#wget pyqt

clean:
	rm -f *.pyc

