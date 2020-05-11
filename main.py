import autopy
import louie
# import threading
import time
# import pynput
from lib.player_keyboard import PlayerKeyboard
from datetime import datetime

class Bot():

	def __init__(self):
		self.screens = [
			Bot.get_bitmap('assets/screen_heroes.png'),
			Bot.get_bitmap('assets/screen_village.png'),
		]
		self.brown_chests = [
			Bot.get_bitmap('assets/chest_brown.png'),
			Bot.get_bitmap('assets/chest_brown2.png'),
			Bot.get_bitmap('assets/chest_brown3.png'),
		]
		self.gold_chests = [
			[
				Bot.get_bitmap('assets/chest_gold_step1.png'),
				Bot.get_bitmap('assets/chest_gold2.png'),
				Bot.get_bitmap('assets/chest_gold3.png'),
			],
			Bot.get_bitmap('assets/chest_gold_step2.png'),
			Bot.get_bitmap('assets/chest_gold_step3.png'),
		]
		self.weapons = [
			Bot.get_bitmap('assets/weapon_swords.png'),
			Bot.get_bitmap('assets/weapon_daggers.png'),
			Bot.get_bitmap('assets/weapon_blobs.png'),
			Bot.get_bitmap('assets/weapon_fireball.png'),
			Bot.get_bitmap('assets/weapon_katana.png'),
		]

		self.decline = Bot.get_bitmap('assets/decline.png')
		self.cta_app = Bot.get_bitmap('assets/crush_them_all_app.png')

		self.escape_menus = [
			self.cta_app,
			self.decline,
			Bot.get_bitmap('assets/okay.png'),
			Bot.get_bitmap('assets/X.png'),
			Bot.get_bitmap('assets/chest_gold_step3.png'),
		]
		self.functions = [
			Bot.get_bitmap('assets/function_upgrade_heroes.png'),
			Bot.get_bitmap('assets/function_upgrade_villages.png'),
		]
		self.collections = [
			Bot.get_bitmap('assets/function_collect.png'),
		]
		self.edge = [Bot.get_bitmap('assets/edge.png')]
		self.edge_loc = None

		self.speedad_steps = [
			Bot.get_bitmap('assets/speedad_step1.png'),
			Bot.get_bitmap('assets/accept.png')
		]

		self.ascend_steps = [
			Bot.get_bitmap('assets/ascend_step1.png'),
			[Bot.get_bitmap('assets/ascend_step2.png')],
			Bot.get_bitmap('assets/ascend_accept.png'),
			Bot.get_bitmap('assets/ascend_step4.png'),
			Bot.get_bitmap('assets/ascend_step5.png')
		]

		self.dungeon_steps = [
			Bot.get_bitmap('assets/screen_battle.png'),
			Bot.get_bitmap('assets/dungeon_step1.png'),
			Bot.get_bitmap('assets/dungeon_step2.png'),
			Bot.get_bitmap('assets/dungeon_step3.png'),
			Bot.get_bitmap('assets/decline.png'),
			Bot.get_bitmap('assets/dungeon_edge.png'),
			Bot.get_bitmap('assets/dungeon_okay.png'),
		]

		self.expedition_steps = [
			Bot.get_bitmap('assets/exped_step0_reward_ready.png'),
			Bot.get_bitmap('assets/screen_battle.png'),
			Bot.get_bitmap('assets/exped_step1.png'),
		]

		self.exped_start = [
			[Bot.get_bitmap('assets/exped_step2_run.png'),
			Bot.get_bitmap('assets/exped_step2_run2.png')],
			Bot.get_bitmap('assets/exped_step3_autofill.png'),
			Bot.get_bitmap('assets/exped_step4_start.png'),
		]

		self.exped_collect = [
			[Bot.get_bitmap('assets/exped_step5_collect.png'),
			Bot.get_bitmap('assets/exped_step5_collect2.png'),
			Bot.get_bitmap('assets/exped_step5_collect3.png')
			],
			Bot.get_bitmap('assets/exped_step6_confirm.png'),
		]

	def stop(self):
		self.stopping = True

	def main(self):
		screen = Bot.refresh_screen()
		screen.save("screen.png")
		# return

		louie.connect(self.stop, signal=PlayerKeyboard.kill_signal)

		self.ideal_ascend_level = 3600
		self.ascend_cooldown = (3000/19)*60
		self.dungeon_cooldown = 800
		self.exped_cooldown = 600
		self.weapon_cooldown = 1
		self.screen_switch_cooldown = 60
		self.functions_cooldown = 20
		
		self.last_dungeon_run = None #datetime.now()
		self.last_exped_run = None #datetime.now()
		self.last_weapon_run = None
		self.last_ascend = datetime.now()
		self.last_screen_switch = None #datetime.now()
		self.last_function_run = None #datetime.now()
		self.stopping = False
		
		self.switch_screens()

		while not self.stopping:
			# start = time.perf_counter()
			self.do_ascend()
			self.do_speedad()
			self.do_dungeon()
			self.do_expedition()
			# print ("standard functions runtime {}".format(time.perf_counter() - start))

			# start = time.perf_counter()
			self.do_chests()
			# print ("chest 1 runtime {}".format(time.perf_counter() - start))
			# start = time.perf_counter()
			self.do_edge()
			# print ("edge runtime {}".format(time.perf_counter() - start))
			# start = time.perf_counter()
			self.do_chests()
			# print ("chest 2 runtime {}".format(time.perf_counter() - start))
			# start = time.perf_counter()
			self.do_weapons()
			# print ("weapons runtime {}".format(time.perf_counter() - start))
			
			# start = time.perf_counter()
			self.switch_screens()
			# print ("switch screens runtime {}".format(time.perf_counter() - start))
			# start = time.perf_counter()
			self.do_functions()
			# print ("routine runtime {}".format(time.perf_counter() - start))
			# return

	def do_expedition(self):
		reward_ready = Bot.find_asset(self.expedition_steps[0], tolerance=0.2)

		if reward_ready or Bot.check_cooldown(self.last_exped_run, self.exped_cooldown):
			in_exped = Bot.do_steps([self.expedition_steps[1], self.expedition_steps[2]])
			Bot.do_steps(self.exped_collect, loop=True, tolerance=0.3)
			Bot.do_steps(self.exped_start, loop=True, tolerance=0.3)

			if in_exped:
				self.escape_back(self.decline, 2)

			self.last_exped_run = datetime.now()
			Bot.find_and_click_asset(self.screens)
			return True
		return False

	def escape_back(self, back_asset=None, times=1):
		for _ in range(0, times):
			autopy.key.tap(autopy.key.Code.ESCAPE)
			time.sleep(1)

			if Bot.find_and_click_asset(back_asset, tolerance=0.2):
				return True
		return False

	@staticmethod
	def scroll_up_from_asset(assets, distance):
		#toggle click on asset
		#slow move up
		#release click
		return

	def is_out_of_app(self):
		app_screen = self.cta_app

		if Bot.find_asset(assets=app_screen, tolerance=0.2):
			return True
		return False

	def is_in_main_area(self):
		main_area_markers = self.screens

		if Bot.find_asset(assets=main_area_markers, tolerance=0.2):
			return True
		return False

	def do_dungeon(self):
		if Bot.check_cooldown(self.last_dungeon_run, self.dungeon_cooldown):
			new_dungeon_runtime = datetime.now()

			Bot.do_steps([self.dungeon_steps[0],
					self.dungeon_steps[1],
					self.dungeon_steps[2],
					self.dungeon_steps[3]], delay=0.3)

			decline_found = Bot.find_and_click_asset(self.decline, tolerance=0.2)

			if self.is_in_main_area():
				self.last_dungeon_run = new_dungeon_runtime
				Bot.find_and_click_asset(self.screens)
				return False

			if not decline_found:
				time.sleep(0.5)
				victory = False
				while not victory:
					time.sleep(4)
					victory = self.do_dungeon_boss()

			self.last_dungeon_run = new_dungeon_runtime
			Bot.find_and_click_asset(self.screens)
			return True
		return False

			# do_dungeon_boss(dunweapons, edge)
			# autopy.key.tap(autopy.key.Code.ESCAPE)

		# find_and_click_asset(dungeon_steps[4])
		# reward_accepted = False
		# while not reward_accepted:
		# 	time.sleep(3)
		# 	reward_accepted = find_and_click_asset(dungeon_steps[4])


	def do_dungeon_boss(self):
		# weapons, dungeon_steps[5], dungeon_steps[6]
		self.do_weapons()
		time.sleep(1)

		get_rewards = Bot.find_and_click_asset(self.dungeon_steps[6], tolerance=0.2)
		if not get_rewards:
			return False
		return True

	def do_ascend(self):
		if Bot.check_cooldown(self.last_ascend, self.ascend_cooldown, log=True):
			if Bot.find_and_click_asset(self.ascend_steps[0], 3, tolerance=0.2, persistent=True):
				if Bot.find_and_click_asset(self.ascend_steps[1]):
					Bot.find_and_click_asset(self.ascend_steps[2])
					time.sleep(5)
					self.escape_back(self.decline)
					time.sleep(1)
					self.escape_back(self.decline)
					time.sleep(1)
					self.escape_back(self.decline)
					time.sleep(1)
					self.ascend_cooldown = (self.ideal_ascend_level/19)*60
					self.last_ascend = datetime.now()
					time.sleep(1)
					return True
		return False

	def do_speedad(self):
		speedad_ready = Bot.find_and_click_asset(self.speedad_steps[0], tolerance=0.2)

		if speedad_ready:
			ad_launched = self.launch_ad(self.speedad_steps[1])
		
			if ad_launched:
				return True
		
		return False

	def launch_ad(self, ad_asset, timeout=7):
		ad_confirm = Bot.find_and_click_asset(ad_asset, tolerance=0.2)
		if ad_confirm:
			time.sleep(timeout)

			#check to see if the ad launched properly (look for ascend?)
			if self.is_in_main_area():
				return False
			
			#check to see if we crashed
			if Bot.find_asset(None, self.cta_app, tolerance=0.2):
				self.restart_app()
				return False

			ad_complete = False
			adtimeout = 60
			adstart = datetime.now()
			while not ad_complete :
				if Bot.check_cooldown(adstart, adtimeout):
					print("restarting app")
					self.restart_app()
					return False
				ad_complete = self.check_if_ad_is_done(7)

				if ad_complete:
					return True
		else:
			return False

	def restart_app(self):
		self.exit_app()
		self.open_app()
		time.sleep(10)

	def open_app(self):
		app_opened = False
		while not app_opened:
			app_opened = Bot.find_and_click_asset(self.cta_app)
		print ("app opened")

	def exit_app(self):
		while not self.is_out_of_app():
			autopy.key.tap(autopy.key.Code.PAGE_UP)
			time.sleep(5) #takes a while for the X to appear
			Bot.find_and_click_asset(Bot.get_bitmap("assets/gamequit.png"), tolerance=0.2)
			time.sleep(10)
		
	def check_if_ad_is_done(self, timeout):
		resume_button = [
						Bot.get_bitmap("assets/ad_resume.png"), 
						Bot.get_bitmap("assets/ad_resume2.png"),
						Bot.get_bitmap("assets/ad_resume3.png"),
						]

		resume_found = self.escape_back(resume_button)

		if resume_found:
			time.sleep(timeout)
			return False
		else:
			return self.is_in_main_area()
			# screen = Bot.refresh_screen()
			# ad_complete_needle = get_bitmap('assets/screen_battle.png')
			# ad_complete = find_asset(screen, ad_complete_needle, tolerance=0.2)
			# if ad_complete:
			# 	return True
			# else:
			# 	return False

	def do_chests(self, do_gold_chests=True):
		screen = Bot.refresh_screen(False)
		Bot.find_and_click_asset(self.brown_chests, tolerance=0.3, screen=screen)	

		if do_gold_chests:
			gold_chest_clicked = Bot.find_and_click_asset(self.gold_chests[0], tolerance=0.3, screen=screen)

			if gold_chest_clicked:
				time.sleep(0.2)
				if self.launch_ad(self.gold_chests[1]):
					time.sleep(1)
					Bot.find_and_click_asset(self.gold_chests[2])

	def switch_screens(self):
		if Bot.check_cooldown(self.last_screen_switch, self.screen_switch_cooldown):
			Bot.find_and_click_asset(self.screens)
			self.last_screen_switch = datetime.now()

	def do_weapons(self, tolerance=0):
		screen = Bot.refresh_screen(False)
		if Bot.check_cooldown(self.last_weapon_run, self.weapon_cooldown):
			if self.do_edge(screen):
				if Bot.find_and_click_asset(self.weapons, tolerance=0, screen=screen):
					self.last_weapon_run = datetime.now()
					return True
		return False

	def do_edge(self, screen=None):
		if self.edge_loc is None:
			if screen is None:
				screen = Bot.refresh_screen(False)
			self.edge_loc = Bot.find_asset(screen, self.edge)
		
		return Bot.find_and_click_asset(self.edge, yoffset=-35, screen=screen)

	def do_functions(self):
		if Bot.check_cooldown(self.last_function_run, self.functions_cooldown):
			Bot.find_and_click_asset(self.collections, 2, tolerance=0.2)
			Bot.find_and_click_asset(self.functions, 5, tolerance=0.1)
			Bot.find_and_click_asset(self.escape_menus, tolerance=0.2)
			self.last_function_run = datetime.now()

	@staticmethod
	def do_steps(steps, delay=1, loop=False, tolerance=0.2):
		completed_once = False
		clicked_step = True
		while clicked_step:
			for step in steps:
				step_done = Bot.find_and_click_asset(step, tolerance=tolerance)

				if not step_done:
					clicked_step = False
					continue
				time.sleep(delay)
			if step_done:
				completed_once = True
				if not loop:
					break
		return completed_once

	@staticmethod
	def find_and_click_asset(assets, click_x_times=1, xoffset=0, yoffset=0, tolerance=0, persistent=False, sleep_after_click=0.2, screen=None):
		count = 1

		if persistent:
			count = 5

		for _ in range(0, count):
			if screen is None:
				screen = Bot.refresh_screen()
			asset = Bot.find_asset(screen, assets, tolerance)
			if asset:
				Bot.click_asset(asset, click_x_times, xoffset, yoffset, sleep_after_click)
				time.sleep(0.1)
				return True
		return False

	@staticmethod
	def find_asset(screen=None, assets=None, tolerance=0):
		if assets is None:
			return None

		if screen is None:
			screen = Bot.refresh_screen()

		if isinstance(assets, list):
			for asset in assets:
				found_asset = screen.find_bitmap(asset, tolerance)
				if found_asset:
					return found_asset
		else:
			found_asset = screen.find_bitmap(assets, tolerance)
			if found_asset:
				return found_asset

		return None

	@staticmethod
	def find_every_asset(screen, assets):
		found_assets = []

		for asset in assets:
			found_asset = screen.find_every_bitmap(asset)
			if found_asset:
				found_assets.append(found_asset)

		return found_assets

	@staticmethod
	def click_asset(found_asset, count=1, xoffset=0, yoffset=0, sleep_after_click=0.1):
		autopy.mouse.move(found_asset[0]+xoffset, found_asset[1]+yoffset)
		for _ in range(0,count):
			autopy.mouse.click()
			time.sleep(sleep_after_click)

	@staticmethod
	def get_bitmap(file):
		return autopy.bitmap.Bitmap.open(file)

	@staticmethod
	def refresh_screen(full=True):
		screen = None
		if full:
			screen = autopy.bitmap.capture_screen(((0,0), (390,730)))
		else:
			screen = autopy.bitmap.capture_screen(((0,0), (390,380)))
		return screen

	@staticmethod
	def check_cooldown(last_use, cooldown, log=False):
		if not last_use:
			return True
		timer = datetime.now() - last_use
		seconds = timer.total_seconds()

		if log:
			next_asc_minutes = round((cooldown - seconds) / 60, 2)
			print(str(next_asc_minutes))
			f = open("log.txt", "w")
			f.write("Python bot for mobile game:\ncrush them all\n\nNext ascend in:\n{} minutes.".format(str(next_asc_minutes)))
			f.close()

		if seconds > cooldown:
			return True
		return False

if __name__ == '__main__':
	P = PlayerKeyboard()
	P.start()
	bot = Bot()
	bot.main()