SRC	=	main.py

NAME	=	pbrain-gomoku-ai

all:
	pip3 install --user -r requirements.txt
	pyinstaller -F --distpath ./ --name $(NAME) $(SRC)

clean:
	rm -r -f ./__pycache__ *.spec ./build ./dist

fclean : clean
	rm $(NAME)

re:	fclean	all