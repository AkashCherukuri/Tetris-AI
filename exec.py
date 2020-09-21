from game.core import tetris
from bot import T_bot
#from bot import *

if __name__ == "__main__":
	choice = input('Enter 0 to play Tetris and 1 to give us that satisfaction: ')
	if (choice == '0'):
		g = tetris()
	elif (choice == '1'):
		g = T_bot()
	else:
		print('All you had to do was enter the damn choice!')
		print('Terminating')
		quit()
	g.run()