
all:
	python3 src/draft.py

load:
	python3 src/load.py

server:
	# source ~/ENV/bin/activate
	# brew services start redis
	# lsof -i:5001
	# kill -9 PID
	# # Delete all files in migrations folder
	# # Delete all rows in portal/db.sqlite3 -> django_migrations
	# python src/portal/manage.py makemigrations catan
	# python src/portal/manage.py migrate catan --database=catan
	python src/portal/manage.py runserver 0.0.0.0:5001

readme:
	python3 ../latex/create_book.py --path README.md --name 桌游类小游戏开发框架 --author "南方小智，Michael Gu" --output wiki
	@echo 'xelatex cmd support Chinese'
	xelatex -output-directory wiki 桌游类小游戏开发框架.tex
	@echo 'run twice to build toc correctly'
	xelatex -output-directory wiki 桌游类小游戏开发框架.tex
	open wiki/桌游类小游戏开发框架.pdf


dot_image:
	dot -Tpng images/README/catan_web_player_state_machine.dot -o images/README/catan_web_player_state_machine.png
	open images/README/catan_web_player_state_machine.png

image:
	python3 ../latex/create_book.py --path wiki/images/test_img.tex --name test --simple --output wiki/images
	xelatex -output-directory wiki/images test.tex
	@echo '需要安装brew install imagemagick'
	convert -density 300 wiki/images/test.pdf -quality 90 wiki/images/test.png
	open wiki/images/test.png

git:
	git push https://github.com/JimmyFromSYSU/boardgame.git master

test:
	python3 ./src/portal/manage.py test catan


# python3 manage.py createsuperuser
# user: zhiliu
# pw: 12345678-Liu
# user: michael
# pw?: 12345678-Gu


# http://127.0.0.1:5001/catan/room/?room_id=6
# http://127.0.0.1:5001/catan/?game_id=8
