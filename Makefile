all: gooe

gooe : gooe.py
	python gooe.py

git:
	git add .
	git commit
	git push

#TODO Maybe include an install directive to setup dependencies
install:
	#wget python27
	#wget pyqt

clean:
	rm -f *.pyc

