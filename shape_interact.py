import os
import time
from termcolor import colored
from pynput import keyboard

class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def hitsWall(self, point):
        return point[0] < 0 or point[0] >= self._x or point[1] < 0 or point[1] >= self._y

    def setPos(self, pos, mark):
        self._canvas[pos[0]][pos[1]] = mark

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))

class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.2
        self.pos = [0, 0]

    def up(self):
        pos = [self.pos[0], self.pos[1]-1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def down(self):
        pos = [self.pos[0], self.pos[1]+1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def right(self):
        pos = [self.pos[0]+1, self.pos[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def left(self):
        pos = [self.pos[0]-1, self.pos[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)
        
class Shape(Canvas):
	def __init__(self, canvas):
		self.canvas = canvas
		self.trail = '.'
		self.mark = '*'
		self.framerate = 0.2
		self.pos = [0, 0]
		self.scribe = TerminalScribe(canvas)
		
	def square(self, size):
		"""Draws a square"""
		i = 0
		#go right
		while i < size:
			self.scribe.right()
			i+=1
		i = 0 #re-initalizing i
		#going down
		while i < size:
			self.scribe.down()
			i+=1
		i = 0 #re-initalize
		#going left
		while i < size:
			self.scribe.left()
			i+=1
		i = 0 #re-initalize
		while i < size:
			self.scribe.up()
			i+=1
	
	def rect(self, width, length):
		"""Draws a rectangle"""
		i = 0
		while i < width:
			self.scribe.right()
			i+=1
		i = 0
		while i < length:
			self.scribe.down()
			i+=1
		i = 0
		while i < width:
			self.scribe.left()
			i+=1		
		i = 0
		while i < length:
			self.scribe.up()
			i+=1
		
	def freeroam(self):
		"""allows you to interact with the screen"""
		with keyboard.Events() as events:
			for event in events:
				if event.key == keyboard.Key.right:
					self.scribe.right()
				elif event.key == keyboard.Key.down:
					self.scribe.down()
				elif event.key == keyboard.Key.left:
					self.scribe.left()
				elif event.key == keyboard.Key.up:
					self.scribe.up()
				elif event.key == keyboard.Key.esc:
					break
				
			
        
canvas = Canvas(30, 30)
scribe = TerminalScribe(canvas)
shape = Shape(canvas)

shape.freeroam()
shape.clear()


