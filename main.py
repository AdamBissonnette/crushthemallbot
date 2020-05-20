import autopy
# import louie
import random
# import threading
import time
# import pynput
from lib.player_keyboard import PlayerKeyboard
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

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
			Bot.get_bitmap('assets/weapon_fire.png'),
			Bot.get_bitmap('assets/weapon_light.png'),
			Bot.get_bitmap('assets/weapon_dark.png'),
		]

		self.decline = Bot.get_bitmap('assets/decline.png')
		self.okay = Bot.get_bitmap('assets/okay.png')
		self.cta_app = Bot.get_bitmap('assets/crush_them_all_app.png')
		self.os_error = Bot.get_bitmap('assets/crash_game_stopped.png')
		self.signed_out = Bot.get_bitmap('assets/app_signed_out.png')
		self.screen_saver = Bot.get_bitmap('assets/screen_saver2.png')

		self.escape_menus = [
			self.cta_app,
			self.decline,
			self.okay,
			Bot.get_bitmap('assets/away_okay.png'),
			Bot.get_bitmap('assets/X.png'),
			Bot.get_bitmap('assets/X2.png'),
			Bot.get_bitmap('assets/chest_gold_step3.png'),
			self.os_error,
			self.screen_saver,
			Bot.get_bitmap('assets/game_still_running_okay2.png'),
		]
		self.functions = [
			Bot.get_bitmap('assets/function_upgrade_heroes.png'),
			Bot.get_bitmap('assets/function_upgrade_villages.png'),
		]

		self.upgrade_heroes = [
			Bot.get_bitmap('assets/function_upgrade_heroes.png'),
			Bot.get_bitmap('assets/function_upgrade_heroes2.png'),
		]

		self.collections = [
			Bot.get_bitmap('assets/function_collect.png'),
		]
		self.edge = [Bot.get_bitmap('assets/edge.png')]
		self.edge_loc = None

		self.new_stage = [
			Bot.get_bitmap('assets/new_stage.png'), 
			Bot.get_bitmap('assets/new_stage2.png'), 
			Bot.get_bitmap('assets/new_stage3.png'), 
		]

		self.speedad_steps = [
			Bot.get_bitmap('assets/speedad_step1.png'),
			Bot.get_bitmap('assets/accept.png')
		]

		self.ascend_steps = [
			Bot.get_bitmap('assets/ascend_step1.png'),
			[
				# Bot.get_bitmap('assets/ascend_step2.png'),
				Bot.get_bitmap('assets/ascend_step2_double.png')
			],
			Bot.get_bitmap('assets/ascend_accept.png'),
			Bot.get_bitmap('assets/ascend_step4.png'),
			Bot.get_bitmap('assets/ascend_step5.png')
		]

		self.dungeon_steps = [
			Bot.get_bitmap('assets/screen_battle.png'),
			Bot.get_bitmap('assets/dungeon_step1.png'),
			# Bot.get_bitmap('assets/dungeon_step2.png'),
			[Bot.get_bitmap('assets/dungeon_step2.png'),
				Bot.get_bitmap('assets/dungeon_step2_alt.png')], #top or mid dungeon
			Bot.get_bitmap('assets/dungeon_step3.png'), #highest rank dungeon
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

		self.guild_chat = [
			Bot.get_bitmap('assets/screen_guild.png'),
			Bot.get_bitmap('assets/guild_chat.png'),
		]

		self.guild_medals_collect = [
			Bot.get_bitmap('assets/guild_medals_collect.png')
		]

		self.guild_medals_help = [
			Bot.get_bitmap('assets/guild_medals_help.png')
		]

		self.guild_medals_request = [
			Bot.get_bitmap('assets/guild_medal_request.png'),
			Bot.get_bitmap('assets/guild_medal.png'),
			Bot.get_bitmap('assets/guild_medal_request3.png'),
		]

		self.guild_dungeon = [
			#dungeon
			#click banner
			#attack once? twice?
		]

		self.mail = [
			Bot.get_bitmap('assets/mail_step1.png'),
			Bot.get_bitmap('assets/mail_step2.png'),
			Bot.get_bitmap('assets/mail_mailbox.png'),
		]

		self.mail_collect = [
			Bot.get_bitmap('assets/mail_step3.png'),
			Bot.get_bitmap('assets/mail_step4.png'), #select all
		]

		self.gift_collect = [
			Bot.get_bitmap('assets/mail_step5.png'), 
			Bot.get_bitmap('assets/mail_step3.png'), #select all
			Bot.get_bitmap('assets/mail_step7.png'),
		]

	def stop(self):
		self.stopping = True

	@staticmethod
	def test_debug_stage_images():
		from os import walk

		f = []
		for (dirpath, dirnames, filenames) in walk('./debug'):
			f.extend(filenames)
			break
		
		i = 0
		for name in filenames:
			if "out" not in name:
				text, image = Bot.get_stage_number('debug/'+name, True)
				print(name, text, text in name and len(text) > 1)
				i = i + 1
			
			# if i >= 10:
			# 	return

	def main(self):
		screen = Bot.refresh_screen()
		screen.save("screen.png")

		# Bot.test_debug_stage_images()

		# return
		# self.check_for_sign_out()

		self.last_stage_check = None
		self.stage_reports = []
		self.target_stage = 4050
		self.ascend_cooldown = 60
		self.dungeon_cooldown = 800
		self.exped_cooldown = 600
		self.weapon_cooldown = 0.5
		self.screen_switch_cooldown = 120
		self.functions_cooldown = 30
		self.guild_medal_cooldown = 900
		self.signed_out_check_cooldown = 60

		self.last_guild_medal_run = Bot.get_timestamp()
		self.last_dungeon_run = Bot.get_timestamp()
		self.last_exped_run = Bot.get_timestamp()
		self.last_weapon_run = None
		self.last_ascend_check = None #Bot.get_timestamp()
		self.last_screen_switch = None #Bot.get_timestamp()
		self.last_function_run = Bot.get_timestamp()
		self.last_signed_out_check = None
		self.stopping = False
		
		self.switch_screens()

		while not self.stopping:
			# self.do_mail()
			# return
			# start = Bot.get_timestamp()
			self.check_for_sign_out()
			# Bot.check_perf("routines ", start)
			self.do_ascend()
			self.do_speedad()
			self.do_dungeon()
			self.do_expedition()
			self.do_guild_medals()
			

			if self.stopping:
				continue

			# start = Bot.get_timestamp()
			self.do_chests()
			self.do_edge()
			# Bot.check_perf("chests ", start)
			if self.stopping:
				continue

			# start = Bot.get_timestamp()
			weapons_done = self.do_weapons()
			# Bot.check_perf("weapons", start)

			if self.stopping:
				continue
			
			self.switch_screens()
			self.do_functions()
			# time.sleep(0.5) #maybe have this ??

	@staticmethod
	def get_timestamp():
		return time.perf_counter()

	@staticmethod
	def check_perf(note, seconds, debug=True):
		if debug:
			curTime = Bot.get_timestamp()
			print(note, curTime, seconds, (curTime-seconds)*1000)

	def check_for_sign_out(self):
		if Bot.check_cooldown(self.last_signed_out_check, self.signed_out_check_cooldown):
			signed_out = Bot.find_asset(None, self.signed_out, tolerance=0.2)
			if signed_out:
				print("signed out of app - restarting")
				#wait 15 minutes before re-opening the app
				self.restart_app(900)
				self.last_signed_out_check = Bot.get_timestamp()

	def max_level_heroes(self):
		level_up = Bot.find_asset(None, self.upgrade_heroes[0], tolerance=0.2)
		Bot.click_asset(level_up, toggle_state=1, sleep_after_click=1, xoffset=30)
		Bot.click_asset(level_up, toggle_state=2, sleep_after_click=1,
					xoffset=-20, yoffset=-20)
		derp = Bot.find_asset(None, self.upgrade_heroes[1], tolerance=0.2)
		print(derp)
		Bot.click_asset(derp, 2, xoffset=20)

	def do_mail(self):
		Bot.do_steps(
			self.mail,
			delay=1,
			tolerance=0
		)

		Bot.do_steps(
			self.mail_collect,
			delay=2,
			tolerance=0
		)

		Bot.do_steps(
			self.gift_collect,
			delay=2,
			tolerance=0.2
		)

		self.escape_back(self.decline, 2)
		self.last_mail_run = Bot.get_timestamp()

	def do_guild_medals(self):
		#goto guild chat
		if Bot.check_cooldown(self.last_guild_medal_run, self.guild_medal_cooldown):
			Bot.do_steps(self.guild_chat)
			
			Bot.do_steps(self.guild_medals_collect)

			Bot.do_steps(self.guild_medals_help, loop=True, tolerance=0.3, delay=1)

			Bot.do_steps(self.guild_medals_request)

			self.escape_back(self.decline, 2)
			self.last_guild_medal_run = Bot.get_timestamp()

	def do_expedition(self):
		reward_ready = Bot.find_asset(None, self.expedition_steps[0], tolerance=0.2)

		if reward_ready or Bot.check_cooldown(self.last_exped_run, self.exped_cooldown):
			in_exped = Bot.do_steps([self.expedition_steps[1], self.expedition_steps[2]])
			Bot.do_steps(self.exped_collect, loop=True, tolerance=0.3, delay=0.5)
			Bot.do_steps(self.exped_start, loop=True, tolerance=0.3, delay=0.5)

			if in_exped:
				self.escape_back(self.decline, 2)

			self.last_exped_run = Bot.get_timestamp()
			Bot.find_and_click_asset(self.screens)
			return True
		return False

	def escape_back(self, back_asset=None, times=1):
		for _ in range(0, times):
			autopy.key.tap(autopy.key.Code.ESCAPE)
			time.sleep(0.5)

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
			new_dungeon_runtime = Bot.get_timestamp()

			Bot.do_steps([self.dungeon_steps[0], self.dungeon_steps[1], self.dungeon_steps[2],
						 self.dungeon_steps[3]], tolerance=0.2, delay=0.5)

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

	def do_math_for_nerds(self):
		stage, screen = Bot.get_stage_number()

		# print(stage)

		stage_number = float(stage)

		stage_difference = 0
		staging_average = 0
		stage_parsed_correctly = True

		if self.last_stage_check is not None:
			stage_difference = stage_number - self.last_stage_check

			#you can't generally go back a large number of stages
			if stage_difference > -300 and stage_difference < 300:
				self.stage_reports.append(stage_difference)
				staging_average = round(sum(self.stage_reports) / len(self.stage_reports), 2)
			else:
				stage_number = self.last_stage_check
				stage_parsed_correctly = False
				screen.save("debug/stage{}.png".format(stage_number))

		self.last_stage_check = stage_number

		percent_complete = str(round((stage_number / self.target_stage) * 100, 3))

		f = open("log.txt", "w")
		ln = "trouble parsing stage #"
		ln2 = ""

		if stage_parsed_correctly:
			ln = ("Percent complete: {}/{} : {}%".format(str(stage_number),
							str(self.target_stage), percent_complete))
			ln2 = ("{} stages since last check, {} avg speed".format(str(stage_difference),
						str(staging_average)))

		f.write("Python bot for mobile game:\ncrush them all\n{}\n{}\n".format(ln, ln2))
		f.close()

		print(ln, ln2)

		return stage_number

	def do_ascend(self):
		ascended = False
		if Bot.check_cooldown(self.last_ascend_check, self.ascend_cooldown, log=True):	
			try:
				self.last_ascend_check = Bot.get_timestamp()
				stage_number = self.do_math_for_nerds()

				if stage_number >= self.target_stage:
					if Bot.find_and_click_asset(self.ascend_steps[0], 3, tolerance=0.2, persistent=True):
						if Bot.find_and_click_asset(self.ascend_steps[1]):
							Bot.find_and_click_asset(self.ascend_steps[2])
							time.sleep(5)
							self.escape_back(self.decline)
							time.sleep(1)
							self.escape_back(self.decline)
							time.sleep(1)
							self.escape_back(self.decline)
							time.sleep(5)
							self.switch_screens()
							self.last_stage_check = None
							self.stage_reports = []
							ascended = True
			except Exception as e:
				print(e)
		return ascended

	def do_speedad(self):
		speedad_ready = Bot.find_and_click_asset(self.speedad_steps[0], tolerance=0.2)

		if speedad_ready:
			ad_launched = self.launch_ad(self.speedad_steps[1])
		
			if ad_launched:
				return True
		
		return False

	def launch_ad(self, ad_asset, timeout=7):
		ad_confirm = Bot.find_and_click_asset(ad_asset, tolerance=0.2, persistent=True)
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
			adtimeout = 90
			adstart = Bot.get_timestamp()
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

	def restart_app(self, delay=0.2):
		self.exit_app()
		time.sleep(delay)
		self.open_app()
		time.sleep(10)

	def open_app(self):
		app_opened = False
		while not app_opened and not self.is_in_main_area():
			print("tryin ta open app")
			app_opened = Bot.find_and_click_asset(self.cta_app, tolerance=0.2)
			time.sleep(1)

		self.clear_menus()		
		
		print ("app opened")

	def clear_menus(self):
		menus_showing = True
		is_in_main_area = False
		while menus_showing or not is_in_main_area:
			print("looking to clear menus")
			is_in_main_area = self.is_in_main_area()
			menus_showing = Bot.find_and_click_asset(self.escape_menus, tolerance=0.2)
			time.sleep(1)
			print("Menu found", menus_showing and not is_in_main_area)
			if not menus_showing:
				self.escape_back(self.decline, 2)
	
	def exit_app(self):
		while not self.is_out_of_app():
			print("tryin ta leave app")
			Bot.find_and_click_asset(self.os_error, tolerance=0.2)
			time.sleep(2)
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

	def do_chests(self, screen=None, do_gold_chests=True):
		if screen is None:
			screen = Bot.refresh_screen(3)
		found_chest = Bot.find_and_click_asset(self.brown_chests, tolerance=0.3, screen=screen, yoffset=125)

		if not found_chest and do_gold_chests:
			gold_chest_clicked = Bot.find_and_click_asset(self.gold_chests[0], tolerance=0.3, screen=screen, yoffset=125)

			if gold_chest_clicked:
				time.sleep(0.2)
				if self.launch_ad(self.gold_chests[1]):
					time.sleep(1)
					Bot.find_and_click_asset(self.gold_chests[2])

	def switch_screens(self, force_switch=False):
		if force_switch or Bot.check_cooldown(self.last_screen_switch, self.screen_switch_cooldown):
			Bot.find_and_click_asset(self.screens)
			self.last_screen_switch = Bot.get_timestamp()
			return True
		return False

	def do_weapons(self, tolerance=0):
		screen = Bot.refresh_screen(3)
		self.do_chests(screen)
		used_weapon = False
		if Bot.check_cooldown(self.last_weapon_run, self.weapon_cooldown):
			if self.do_edge(screen):
				# screen = Bot.refresh_screen(3)
				if Bot.find_and_click_asset(self.weapons, tolerance=0, screen=screen, yoffset=125):
					self.last_weapon_run = Bot.get_timestamp()
					used_weapon = True
				# self.do_chests(screen)
		return used_weapon

	def do_edge(self, screen=None):
		if screen is None:
			screen = Bot.refresh_screen(3)

		if self.edge_loc is None:
			self.switch_screens(True)
			self.edge_loc = Bot.find_asset(screen, self.edge)
		
		edge_found = Bot.find_and_click_asset(self.edge, yoffset=95, screen=screen)

		if not edge_found:
			self.edge_loc = None

		return edge_found

	def do_functions(self, other_functions_done=True):
		if not other_functions_done or Bot.check_cooldown(self.last_function_run, self.functions_cooldown):
			Bot.find_and_click_asset(self.collections, tolerance=0.2)
			Bot.find_and_click_asset(self.functions, 5, tolerance=0.1)
			self.do_chests()
			Bot.do_steps(self.escape_menus, 1, True)
			
			self.last_function_run = Bot.get_timestamp()
			
			return True
		return False

	@staticmethod
	def get_stage_number(imPath=None, output=False):
		screen = None
		if imPath is None:
			screen = Bot.refresh_screen(4)
			screen.save("stage.png")
			imPath = "stage.png"


		pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
		im = Image.open(imPath)

		im = im.convert("RGBA")
		newimdata = []
		datas = im.getdata()

		im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
		enhancer = ImageEnhance.Contrast(im)
		im = enhancer.enhance(5)

		for item in datas:
			if item[0] > 175 or item[1] > 175 or item[2] > 175:
				newimdata.append((0,0,0))
			else:
				newimdata.append((255, 255, 255))
		im.putdata(newimdata)

		im = im.convert('1')

		text = pytesseract.image_to_string(im,config='-c tessedit_char_whitelist=0123456789 --psm 6', lang='eng')

		# if output:
		# 	im.save("{}.{}.out.png".format(imPath,text))

		return text, screen

	@staticmethod
	def do_steps(steps, delay=0.5, loop=False, tolerance=0.2):
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
	def find_and_click_asset(assets, click_x_times=1, xoffset=0, yoffset=0,
							tolerance=0, persistent=False, sleep_after_click=0.2,
							screen=None, toggle_state=0):
		clicked = False
		click_attempted = False
		while not clicked:
			if screen is None:
				screen = Bot.refresh_screen()
			asset = Bot.find_asset(screen, assets, tolerance)
			if asset:
				Bot.click_asset(asset, click_x_times, xoffset, yoffset, sleep_after_click, toggle_state)
				time.sleep(0.1)
				click_attempted = True
			else:
				if click_attempted:
					clicked = True
				else:
					clicked = False
					break
			screen = None
			if not persistent:
				clicked = True
			else:
				time.sleep(0.5)

		return clicked

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
	def find_every_asset(assets, screen=None):
		found_assets = []

		if assets is None:
			return []

		if screen is None:
			screen = Bot.refresh_screen()

		if isinstance(assets, list):
			for asset in assets:
				found_asset = screen.find_every_bitmap(asset)
				if found_asset:
					found_assets.append(found_asset)
		else:
			found_assets = screen.find_every_bitmap(assets)

		return found_assets

	@staticmethod
	def click_asset(found_asset, count=1, xoffset=0, yoffset=0,
					 sleep_after_click=0.1, toggle_state=0):
		autopy.mouse.move(found_asset[0]+xoffset, found_asset[1]+yoffset)
		for _ in range(0,count):
			if toggle_state == 0:
				autopy.mouse.click()
			elif toggle_state == 1:
				autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
			elif toggle_state == 2:
				autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
			time.sleep(sleep_after_click)

	@staticmethod
	def get_bitmap(file):
		return autopy.bitmap.Bitmap.open(file)

	@staticmethod
	def refresh_screen(size=1):
		screen = None
		if size == 1:
			screen = autopy.bitmap.capture_screen(((0,0), (390,730)))
		elif size == 2:
			screen = autopy.bitmap.capture_screen(((0,0), (390,350)))
			screen = autopy.bitmap.capture_screen(((0,0), (390,730)))
		elif size == 3:
			screen = autopy.bitmap.capture_screen(((0,125), (390,225)))
		else:
			screen = autopy.bitmap.capture_screen(((197,30), (40,30)))
		return screen

	@staticmethod
	def check_cooldown(last_use, cooldown, log=False):
		start = Bot.get_timestamp()
		is_expired = False
		if not last_use:
			return True
		timer = Bot.get_timestamp() - last_use
		seconds = timer

		# if log:
		# 	next_asc_minutes = round((cooldown - seconds) / 60, 2)
		# 	print(str(next_asc_minutes))

		if seconds > cooldown:
			is_expired = True
		# Bot.check_perf("cooldown", start, False)
		return is_expired

if __name__ == '__main__':
	bot = Bot()
	P = PlayerKeyboard(bot)
	P.start()
	bot.main()