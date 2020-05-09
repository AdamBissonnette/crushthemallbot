import autopy
import louie
import time
from lib.thread import Thread

class Screen(Thread):

	signal_found_brown_chest = 'screen.found_brown_chest'
	signal_found_gold_chest = 'screen.found_gold_chest'
	signal_found_ability = 'screen.found_ability'
	signal_found_new_stage = 'screen.found_new_stage'
	signal_found_edge = 'screen.found_edge'
	
	signal_find_abilities = 'screen.find_abilities'
	signal_find_chests = 'screen.find_chests'

	screen_top = None
	screen_full = None
	brown_chests = None
	gold_chests = None
	abilities = None
	new_stage = None
	edge = None

	def __init__(self, brown_chests, gold_chests, abilities, new_stage, edge):
		super().__init__()
		self.timeout = 0.05

		self.brown_chests = brown_chests
		self.gold_chests = gold_chests
		self.abilities = abilities
		self.new_stage = new_stage
		self.edge = edge

		# print(brown_chests, gold_chests, abilities, new_stage, edge)
	
	def refresh_screen(self):
		self.screen_top = autopy.bitmap.capture_screen(((0,0), (390,340)))
		# self.screen_full = autopy.bitmap.capture_screen(((0,0), (390,730)))
	
	@staticmethod
	def find_asset(screen, assets, tolerance, signal):
		if assets is None:
			return None

		if isinstance(assets, list):
			for asset in assets:
				found_asset = screen.find_bitmap(asset, tolerance)
				if found_asset:
					# print("{} {}".format(signal, str(found_asset)))
					louie.send(data=found_asset, signal=signal)
					return True
		else:
			found_asset = screen.find_bitmap(assets, tolerance)
			if found_asset:
				# print("{} {}".format(signal, str(found_asset)))
				louie.send(data=found_asset, signal=signal)
				return True
		return False

	@staticmethod
	def find_every_asset(screen, assets, tolerance, signal):
		found_assets = []

		for asset in assets:
			found_asset = screen.find_bitmap(asset, tolerance)
			if found_asset:
				# print("{} {}".format(signal, str(found_asset)))
				found_assets.append(found_asset)

		louie.send(data=found_assets, signal=signal)

	def do_action(self):
		self.refresh_screen()
		if self.find_asset(self.screen_top, self.new_stage, 0.2, Screen.signal_found_new_stage):
			self.find_every_asset(self.screen_top, self.abilities, 0, Screen.signal_found_ability)
			time.sleep(0.2)
			self.refresh_screen()
			self.find_asset(self.screen_top, self.edge, 0.2, Screen.signal_found_edge)
			self.find_asset(self.screen_top, self.brown_chests, 0.2, Screen.signal_found_brown_chest)
			self.find_asset(self.screen_top, self.gold_chests, 0.2, Screen.signal_found_gold_chest)

