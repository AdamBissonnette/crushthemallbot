import louie
from pynput import keyboard
from lib.thread import Thread
import atexit

class PlayerKeyboard(Thread):

	keyboard = None
	bot = None
	def __init__(self, bot):
		super().__init__()
		self.timeout = 0.2
		self.stopping = False
		self.bot = bot
	
	def on_press(self, key):
		pass

	def on_release(self, key):
		if key == keyboard.Key.end:
			self.stopping = True
			self.bot.stop()
			return False

	def do_action(self):
		with keyboard.Listener(
			on_press=self.on_press,
			on_release=self.on_release) as listener:
			listener.join()