all:
	python3 src/draft.py

readme:
	python3 ../latex/create_book.py --path README.md --name 桌游类小游戏开发框架 --author "南方小智" --output wiki
	@echo 'xelatex cmd support Chinese'
	xelatex -output-directory wiki 桌游类小游戏开发框架.tex
	@echo 'run twice to build toc correctly'
	xelatex -output-directory wiki 桌游类小游戏开发框架.tex
	open wiki/桌游类小游戏开发框架.pdf

image:
	python3 ../latex/create_book.py --path wiki/images/image0.tex --name 三角形 --simple --output wiki/images
	xelatex -output-directory wiki/images 三角形.tex
	@echo '需要安装brew install imagemagick'
	convert -density 300 wiki/images/三角形.pdf -quality 90 wiki/images/三角形.png
	open wiki/images/三角形.png
