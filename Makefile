SRC	=	main.py

NAME	=	pbrain-gomoku-ai

all:
	cp $(SRC) $(NAME)
	chmod +x $(NAME)

clean:
	rm -rf **/__pycache__ **/*.pyc

fclean : clean
	rm $(NAME)

re:	fclean	all