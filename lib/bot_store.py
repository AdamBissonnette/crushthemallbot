import louie
import time
from datetime import datetime
from lib.thread import Thread
from lib.screen import Screen

class BotStore():

	brown_chest = None
	gold_chest = None
	ability = []
	edge = None
	new_stage_time = None
	ability_used_in_stage = False
	at_right_screen_edge = False

	def __init__(self):
		super().__init__()
		self.timeout = 1

		louie.connect(self.set_brown_chest, signal=Screen.signal_found_brown_chest)
		louie.connect(self.set_gold_chest, signal=Screen.signal_found_gold_chest)
		louie.connect(self.set_ability, signal=Screen.signal_found_ability)
		louie.connect(self.set_new_stage, signal=Screen.signal_found_new_stage)
		louie.connect(self.set_edge, signal=Screen.signal_found_edge)

	def set_brown_chest(self, data):
		self.brown_chest = data

	def set_gold_chest(self, data):
		self.gold_chest = data

	def set_edge(self, data):
		self.edge = data

	def set_ability(self, data):
		# print(data)
		self.ability = data

	def set_new_stage(self):
		print("new stage found")
		self.brown_chest = None
		self.gold_chest = None
		self.ability_used_in_stage = False
		self.at_right_screen_edge = False
		self.new_stage_time = datetime.now()
