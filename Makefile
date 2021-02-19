SRC	=	main.py

NAME	=	pbrain-gomoku-ai

all:
	cp $(SRC) $(NAME)
	chmod +x $(NAME)

clean:
	rm -r -f ./__pycache__

fclean : clean
	rm -f $(NAME)

re:	fclean	all