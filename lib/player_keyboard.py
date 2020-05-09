import louie
from pynput import keyboard
from lib.thread import Thread

class PlayerKeyboard(Thread):

	keyboard = None
	def __init__(self):
		super().__init__()
		self.timeout = 0.2
	
	def on_press(self, key):
		if key == keyboard.Key.shift_l:
			self.stopping = True
			louie.send(signal=PlayerKeyboard.kill_signal)
			return False

	def on_release(self, key):
		if key == keyboard.Key.shift_l:
			return False

	def do_action(self):
		listener = keyboard.Listener(
			on_press=self.on_press,
			on_release=self.on_release)
		listener.start()