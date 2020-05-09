from random import random as rnd

import pygame

rand_msgs = ["Saved screenshot0000.png", "Player gained a level", "Friend wants to talk to you"]

class Breadboard: # mirrors Game at a basic level

	def __init__(self):
	
		self.tick = 0
		self.clock = pygame.time.Clock()
		
		self.sys_messages = {}
		self.msg_counter = 0
		
	def add_message(self, message):
	
		self.sys_messages[self.msg_counter] = Sys_Message(self.msg_counter, self, message)
		self.msg_counter += 1
		
	def update(self):
	
		self.clock.tick(60)
		self.tick = (self.tick + 1) % 1048576 # 20 bit number. that should do it
		# there are 5 ticks per second @ 60 ticks
		for msg in self.sys_messages.values():
			msg.update()
			if msg.done: break
	
	def render(self, surface):

		msgs = sorted(self.sys_messages.items())
		for i in range(1,6): # for 5 visible lines
			try:
				y = 475 - 5 * i - font_height * i
				surface.blit(msgs[-i][1].message,(10,y))			
			except:
				break

class Sys_Message:

	def __init__(self, uid, game, message):
		
		self.font = pygame.font.Font(None, 24)

		self.uid = uid	
		self.game = game
	
		self.message = self.font.render(message, 0, (0xff,0xff,0xff))
		self.tick = int(self.game.tick)
		self.fading = True
		self.alpha = 255
		self.done = False
		
	def update(self):
	
		# this would be better done with counting ticks in the main Game class
		self.fading = (self.game.tick - self.tick) >= 160
		self.alpha -= 8 * self.fading * ((self.game.tick - self.tick) % 2 == 0)
		#print(self.alpha)
		if self.alpha <= 0:
			self.alpha = 0
			self.done = True
		self.message.set_alpha(self.alpha)
		
		if self.done:
			del self.game.sys_messages[self.uid]

#def render_sysmsg(messages, surface):

if __name__ == "__main__":

	pygame.init()
	
	display = pygame.display.set_mode((640,480))
	
	bb = Breadboard()
	
	#clock = pygame.time.Clock()
	
	font_height = pygame.font.Font(None, 24).get_height()

	running = True
	while running:
	
		#clock.tick(60)
	
		bb.update()
		
		for event in pygame.event.get():		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					bb.add_message(rand_msgs[int(rnd() * 3)])
				if event.key == pygame.K_ESCAPE:
					running = False
					pygame.quit()
					exit()
		
		bb.render(display)
		pygame.display.flip()
		display.fill((0,0,0))
