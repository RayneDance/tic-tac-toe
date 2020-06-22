import sys, pygame, random, time, math, gameobj, tictactoeengine
pygame.init()

size = width, height = 600,700
white = 255,255,255

screen = pygame.display.set_mode(size)
engine = tictactoeengine.toeEngine()



while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

		if event.type == pygame.MOUSEBUTTONUP:
			engine.updateScoreboard()
			coords = pygame.mouse.get_pos()
			engine.onClick(coords)
	
	screen.fill(white)
	screen.blit(engine.getBoardSurface(), engine.getBoardRect())
	for i in engine.getGameObjects():
			screen.blit(i.getSurface(), i.getCoords())
	for i in engine.getUIComponents():
			screen.blit(i.getSurface(), i.getCoords())
	pygame.display.flip()

