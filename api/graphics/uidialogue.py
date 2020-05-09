import re # REEEEEEEEEEEEEE

import pygame

class UI_Dialogue(object):

	def __init__(self, uid, game, loc, size):
		
		self.uid = uid
		self.game = game
		self.x, self.y = loc
		self.w, self.h = size
		self.visible = False
		self.waiting_for = None
		self.eot = False # end of text_list
		self.text_list = []
		self._returned = False
		
		self.back = pygame.Surface(size).convert_alpha()
		self.back.fill((0,0,0,128))		
		
	def start(self, target=None):
	
		self.eot = False
		self._returned = False
		self.text_line = 0 # an int tracking which Line in the Queue is being iterated over
		self.text_block = 0 # which Block of text from List to be put into Queue
		self.text_range = 3 # the number of Lines to render per Block
		self.writing = True
		self.pausing = False
		self.pause_count = 0

		if target: self.text_list = target.dialogueLines # TODO TODO TODO
		self.setup()
		
		self.visible = True
		self.game.controller.flush()
		
	def setup(self):
	
		self.text_queue = []
		self.text_cursors = []
		
		index = self.text_block
		self.text_queue = self.text_list[index:index+self.text_range]
		
		for i in self.text_queue:
			self.text_cursors.append(0)
		
	def skip(self):
	
		for index, line in enumerate(self.text_queue):
			self.text_cursors[index] = len(line)
		
		self.text_line = 0	
		self.text_block += self.text_range
		
	def stop(self):
	
		self.visible = False
		self._returned = True
		self.game.controller.flush()
	
	def base_update(self):
	
		if self.writing and self.visible and self.game.tick % 2 == 0:

			index = self.text_line
			limit = len(self.text_queue[index])
			
			string = self.text_queue[index]
			charPoint = self.text_cursors[index]
			if not self.pausing:
				if string[charPoint:charPoint+1] == ">":
					self.pausing = True
					self.pause_count = pygame.time.get_ticks()
				
				# check to see if there's still text to iterate over
				# and increments the textCursor counter if so
				if self.text_cursors[index] < limit:
					self.text_cursors[index] += 1
					
			if self.pausing:
				if int((pygame.time.get_ticks() - self.pause_count) / 1000) == 1:
					self.pausing = False
					
			# if there is no more text to iterate over
			# we move to the next line in text_queue
			if self.text_cursors[index] == limit:
				self.text_line += 1
			
			# if there is no more text for the last item
			# in text_queue to iterate over we set to move to the next block
			if self.text_cursors[-1] == len(self.text_queue[-1]):
				self.writing = False
				self.text_line = 0
				self.text_block += self.text_range # TODO
				
				if not self.text_list[self.text_block:self.text_block+self.text_range]:
					self.eot = True
							
	def update(self): # override in classes derived
	
		if self.visible: # and self.engine.controlFocus == self:
			aButton = self.game.controller.as_button
		
			if aButton == 1:
				
				if self.writing:
					self.writing = False
					self.skip()
					if not self.text_list[self.text_block:self.text_block+self.text_range]:
						self.eot = True
					
				elif not self.writing:
					self.writing = True
					self.setup()
					
				if not self.text_queue:
					self.writing = False
					self.stop()
			
			#if self.eot:
			#	if self.waiting_for:
			#		self.engine.controlFocus = self.waiting_for
			#		self.waiting_for.start()
			#		if self.waiting_for._returned:
			#			self.engine.stop()

			self.base_update()
			
	def render(self):
	
		if self.visible:
		
			self.game.display.blit(self.back, (self.x, self.y))
	
			for i, l in enumerate(self.text_queue):
				text = l[:self.text_cursors[i]]
				if ">" in text:	text = re.sub(">", "", text)
				rText = self.game.ui_font.render(text, 0, (255,255,255))
				
				x = self.x + 5 # padding
				y = self.y + 5 * (i+1) + i * self.game.ui_font.get_height()
				self.game.display.blit(rText, (x,y))
