# Simple Makefile to compile all lectures
# To compile a specific lecture, run 
#
# make lecture N=X, 
#
# replacing X by an existing number in the source folder.
N=01
all:
	echo "Compiling lectures..."
	python build.py
lecture:
	echo "Compiling lecture aula-$(N).tex"
	python build.py aula-$(N).tex
