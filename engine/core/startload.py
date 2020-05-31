import pygame

class State_StartLoad_Game:

	def __init__(self, game=None):
	
		self.game = game
		
		self.value = 0
		
		self.top_panel = pygame.Surface((300, 32)).convert()
		self.top_panel.fill((0,0,0xff))
		
		self.save_panel = pygame.Surface((300, 96)).convert()
		self.save_panel.fill((0,0,0xff))
		
		self.top_grey = pygame.Surface(self.top_panel.get_size()).convert_alpha()
		self.top_grey.fill((0,0,0,160))
		
		self.save_grey = pygame.Surface(self.save_panel.get_size()).convert_alpha()
		self.save_grey.fill((0,0,0,160))
		
		self.panes = [self.top_panel, self.save_panel, self.save_panel, self.save_panel]
		self.grey_panes = [self.top_grey, self.save_grey, self.save_grey, self.save_grey] 
		
	def render(self, surface):
	
		y = 0
	
		for p, pane in enumerate(self.panes):
			x = 10
			#y = 10 + bool(p) * (self.panes[p-1].get_height() + (10 * p))
			#y = 10 + bool(p) * (10 * p + self.panes[p-1].get_height())
			y += 10 + bool(p) * self.panes[p-1].get_height()
			surface.blit(pane, (x,y))
			if p != self.value: surface.blit(self.grey_panes[p], (x,y))
			
pygame.init()

display = pygame.display.set_mode((640,480))

slg = State_StartLoad_Game()

running = True
while running:

	for event in pygame.event.get():
	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				slg.value = (slg.value + 1) % 4
			if event.key == pygame.K_UP:
				slg.value = (slg.value - 1) % 4

			if event.key == pygame.K_ESCAPE:
				running = False
				pygame.quit()
				exit()
				
			if event.key == pygame.K_RETURN:
				print(slg.value)

	slg.render(display)
	pygame.display.flip()

pygame.time.wait(3000)
