import autopy
# import louie
import random
# import threading
import time
import math
# import pynput
from lib.player_keyboard import PlayerKeyboard
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import win32con
import win32api
import win32ui
import win32gui
import ctypes

class Bot():

	def __init__(self):
		self.window = self.get_window('NoxPlayer')

		self.screens = [
			self.get_bitmap('assets/screen_heroes.png'),
			self.get_bitmap('assets/screen_village.png'),
		]
		self.brown_chests = [
			self.get_bitmap('assets/chest1.png'),
			self.get_bitmap('assets/chest2.png'),
			self.get_bitmap('assets/chest3.png'),
			self.get_bitmap('assets/chest4.png'),
			self.get_bitmap('assets/chest_brown.png'),
			self.get_bitmap('assets/chest_brown2.png'),
			self.get_bitmap('assets/chest_brown3.png'),
		]
		self.gold_chests = [
			[
				self.get_bitmap('assets/chest_gold_step1.png'),
				self.get_bitmap('assets/chest_gold2.png'),
				self.get_bitmap('assets/chest_gold3.png'),
			],
			self.get_bitmap('assets/chest_gold_step2.png'),
			self.get_bitmap('assets/chest_gold_step3.png'),
		]
		self.weapons = [
			self.get_bitmap('assets/weapon_earth.png'),
			self.get_bitmap('assets/weapon_fire.png'),
			self.get_bitmap('assets/weapon_light.png'),
			self.get_bitmap('assets/weapon_swords.png'),
			self.get_bitmap('assets/weapon_dark.png'),
		]

		self.decline = self.get_bitmap('assets/decline.png')
		self.okay = self.get_bitmap('assets/okay.png')
		self.cta_app = self.get_bitmap('assets/crush_them_all_app.png')
		self.os_error = self.get_bitmap('assets/crash_game_stopped.png')
		self.signed_out = self.get_bitmap('assets/app_signed_out.png')
		self.screen_saver = self.get_bitmap('assets/screen_saver2.png')

		self.escape_menus = [
			self.cta_app,
			self.decline,
			self.okay,
			self.get_bitmap('assets/away_okay.png'),
			self.get_bitmap('assets/X.png'),
			self.get_bitmap('assets/X2.png'),
			self.get_bitmap('assets/modal_pack_x.png'),
			self.get_bitmap('assets/chest_gold_step3.png'),
			self.os_error,
			self.screen_saver,
			self.get_bitmap('assets/game_still_running_okay2.png'),
		]
		self.functions = [
			self.get_bitmap('assets/function_upgrade_heroes.png'),
			self.get_bitmap('assets/function_upgrade_villages.png'),
		]

		self.upgrade_heroes = [
			self.get_bitmap('assets/function_upgrade_heroes.png'),
			self.get_bitmap('assets/function_upgrade_heroes2.png'),
		]

		self.collections = [
			self.get_bitmap('assets/function_collect.png'),
		]
		self.edge = [self.get_bitmap('assets/edge.png')]
		self.edge_loc = None

		self.new_stage = [
			self.get_bitmap('assets/new_stage.png'), 
			self.get_bitmap('assets/new_stage2.png'), 
			self.get_bitmap('assets/new_stage3.png'), 
		]

		self.speedad_steps = [
			self.get_bitmap('assets/speedad_step1.png'),
			self.get_bitmap('assets/accept.png')
		]

		self.ascend_steps = [
			self.get_bitmap('assets/ascend_step1.png'),
			[
				# self.get_bitmap('assets/ascend_step2_double.png'),
				self.get_bitmap('assets/ascend_step2.png'),
			],
			self.get_bitmap('assets/ascend_accept.png'),
			self.get_bitmap('assets/ascend_step4.png'),
			self.get_bitmap('assets/ascend_step5.png')
		]

		self.dungeon_steps = [
			self.get_bitmap('assets/screen_battle.png'),
			self.get_bitmap('assets/dungeon_step1.png'),
			# self.get_bitmap('assets/dungeon_step2.png'),
			[
				self.get_bitmap('assets/dungeon_fire.png'),
				# self.get_bitmap('assets/dungeon_step2.png'),
				# self.get_bitmap('assets/dungeon_step2_alt.png'),
				# self.get_bitmap('assets/dungeon_enter.png'),
			], #top or mid or enter button dungeon
			self.get_bitmap('assets/dungeon_step3.png'), #highest rank dungeon
			self.get_bitmap('assets/decline.png'),
			self.get_bitmap('assets/dungeon_edge.png'),
			self.get_bitmap('assets/dungeon_okay.png'),
		]

		self.expedition_steps = [
			self.get_bitmap('assets/exped_step0_reward_ready.png'),
			self.get_bitmap('assets/screen_battle.png'),
			self.get_bitmap('assets/exped_step1.png'),
		]

		self.exped_start = [
			[self.get_bitmap('assets/exped_step2_run.png'),
			self.get_bitmap('assets/exped_step2_run2.png')],
			self.get_bitmap('assets/exped_step3_autofill.png'),
			self.get_bitmap('assets/exped_step4_start.png'),
		]

		self.exped_collect = [
			[self.get_bitmap('assets/exped_step5_collect.png'),
			self.get_bitmap('assets/exped_step5_collect2.png'),
			self.get_bitmap('assets/exped_step5_collect3.png')
			],
			self.get_bitmap('assets/exped_step6_confirm.png'),
		]

		self.guild_chat = [
			self.get_bitmap('assets/screen_guild.png'),
			self.get_bitmap('assets/guild_chat.png'),
		]

		self.guild_medals_collect = [
			self.get_bitmap('assets/guild_medals_collect.png')
		]

		self.guild_medals_help = [
			self.get_bitmap('assets/guild_medals_help.png')
		]

		self.guild_medals_request = [
			self.get_bitmap('assets/guild_medal_request.png'),
			self.get_bitmap('assets/guild_medal.png'),
			self.get_bitmap('assets/guild_medal_request3.png'),
		]

		self.epic_guild_medals_request = [
			self.get_bitmap('assets/guild_medal_request2.png'),
			self.get_bitmap('assets/guild_medal2.png'), 
			self.get_bitmap('assets/guild_medal_request3.png'),
		]

		self.guild_dungeon = [
			#dungeon
			#click banner
			#attack once? twice?
		]

		self.mail = [
			self.get_bitmap('assets/mail_step1.png'),
			self.get_bitmap('assets/mail_step2.png'),
			self.get_bitmap('assets/mail_mailbox.png'),
		]

		self.mail_collect = [
			self.get_bitmap('assets/mail_step3.png'),
			self.get_bitmap('assets/mail_step4.png'), #select all
		]

		self.gift_collect = [
			self.get_bitmap('assets/mail_step5.png'), 
			self.get_bitmap('assets/mail_step3.png'), #select all
			self.get_bitmap('assets/mail_step7.png'),
		]

		self.resume_button = [
				self.get_bitmap("assets/ad_resume.png"), 
				self.get_bitmap("assets/ad_resume2.png"),
				self.get_bitmap("assets/ad_resume3.png"),
				]

		self.ad_exit = [
			self.get_bitmap('assets/ad_exit1.png'),
			self.get_bitmap('assets/ad_exit2.png'),
			self.get_bitmap('assets/ad_exit4.png'),
			self.get_bitmap('assets/ad_exit3.png'),
			self.get_bitmap('assets/ad_exit5.png'),
			self.get_bitmap('assets/ad_exit6.png'),
		]

		self.goldad_steps = [
			self.get_bitmap('assets/screen_shop.png'),
			self.get_bitmap('assets/goldad_step1.png'),
			self.get_bitmap('assets/goldad_end.png'),
		]

		self.goto_blitz = [
			self.get_bitmap('assets/screen_battle.png'),
			self.get_bitmap('assets/screen_blitz.png'),
			# battle screen
			# blitz screen
		]

		self.goto_bliz_tier = [
			self.get_bitmap('assets/blitz_bronze.png'),
			self.get_bitmap('assets/blitz_silver.png'),
			self.get_bitmap('assets/blitz_gold.png'),
		]

		#iterative
		self.do_blitz_rounds = [
			self.get_bitmap('assets/blitz_goto_battle.png'),
			self.get_bitmap('assets/blitz_start_battle.png')
			#accept reward
			#next round
			#next arrow
		]

		self.broken_stages = []

	def stop(self):
		self.stopping = True

	def test_debug_stage_images(self, threshold=100):
		start = time.perf_counter()
		from os import walk

		f = []
		for (dirpath, dirnames, filenames) in walk('./debug'):
			f.extend(filenames)
			break
		
		i = 0
		x = 0
		for name in filenames:
			if "stage40" in name:
				if "out" not in name:
					i = i + 1
					text, image = self.get_stage_number('debug/'+name, True, threshold)
					if image is not None:
						image.save("debug/{}{}.png".format(name,".out.png"))
					if text in name:
						x = x + 1

					# print(name, text, text in name and len(text) > 1)

		print (threshold, x, i, round((x/i) *100, 2), time.perf_counter() - start)				
			
			# if i >= 10:
			# 	return

	def main(self):
		screen = self.refresh_screen()
		screen.save("screen.png")
		# derp = self.find_every_asset([self.get_bitmap('assets/dungeon_enter.png')], screen, 0.35)
		# print (derp)
		# self.test_debug_stage_images(216)
		# self.test_debug_stage_images(218)
		# self.test_debug_stage_images(222)
		# self.test_debug_stage_images(224)

		# derp = self.get_bitmap('assets/guild_medal.png'

		# print (self.find_asset(self.refresh_screen(), self.ad_exit, tolerance=0))
		# # self.find_and_click_asset(self.functions, 5, tolerance=0.1)
		# # self.find_and_click_asset(self.ad_exit, 1, tolerance=0.2)
		# self.weapon_cooldown = 0.5
		# self.last_weapon_run = None
		# self.check_for_sign_out()
		# return

		self.last_stage_check = None
		self.trouble_parsing_stage_count = 0
		self.max_trouble_parsing_count = 20
		self.stage_reports = []
		self.target_stage = 5901
		self.ascend_cooldown = 60
		self.dungeon_cooldown = 600
		self.exped_cooldown = 600
		self.weapon_cooldown = 0.5
		self.blitz_cooldown = 6000
		self.screen_switch_cooldown = 120
		self.functions_cooldown = 60
		self.guild_medal_cooldown = 900
		self.goldad_cooldown = 1800
		self.signed_out_check_cooldown = 30

		self.last_guild_medal_run = self.get_timestamp()
		self.last_dungeon_run = None #self.get_timestamp()
		self.last_exped_run = self.get_timestamp()
		self.last_weapon_run = None
		self.last_goldad_run = self.get_timestamp()
		self.last_ascend_check = None #self.get_timestamp()
		self.last_screen_switch = self.get_timestamp()
		self.last_function_run = self.get_timestamp()
		self.last_signed_out_check = None
		self.last_blitz_run = None
		self.stopping = False

		# self.do_functions()
		# return False
		# self.do_weapons()
		# self.do_speedad()
		# self.do_goldad()
		# self.find_and_click_asset(self.goldad_steps[2])
		# self.do_ascend()
		# needs tuning
		# return
		# self.do_dungeon()
		# self.do_expedition()
		# return

		self.switch_screens()

		while not self.stopping:
			# self.do_mail()
			# return
			# start = self.get_timestamp()
			self.check_for_sign_out()
			# self.check_perf("routines ", start)
			# self.do_blitz()
			# return
			self.do_ascend()
			self.do_speedad()
			self.do_goldad()
			self.do_dungeon()
			self.do_expedition()
			self.do_guild_medals()
			# return
			

			if self.stopping:
				continue

			# start = self.get_timestamp()
			self.do_chests()
			self.do_edge()
			# self.check_perf("chests ", start)
			if self.stopping:
				continue

			# start = self.get_timestamp()
			weapons_done = self.do_weapons()
			# self.check_perf("weapons", start)

			# if not weapons_done:
			# 	self.do_functions(weapons_done)

			if self.stopping:
				continue
			
			self.switch_screens()
			self.do_functions()
			# time.sleep(0.5) #maybe have this ??

	def get_timestamp(self):
		return time.perf_counter()

	def check_perf(self, note, seconds, debug=True):
		if debug:
			curTime = self.get_timestamp()
			print(note, curTime, seconds, (curTime-seconds)*1000)

	def check_for_sign_out(self):
		if self.check_cooldown(self.last_signed_out_check, self.signed_out_check_cooldown):
			signed_out = self.find_asset(None, self.signed_out, tolerance=0.2)
			if signed_out:
				print("signed out of app - restarting")
				#wait 15 minutes before re-opening the app
				self.restart_app(900)
				self.last_signed_out_check = self.get_timestamp()

	def max_level_heroes(self):
		level_up = self.find_asset(None, self.upgrade_heroes[0], tolerance=0.2)
		self.click_asset(level_up, toggle_state=1, sleep_after_click=1, xoffset=30)
		self.click_asset(level_up, toggle_state=2, sleep_after_click=1,
					xoffset=-20, yoffset=-20)
		derp = self.find_asset(None, self.upgrade_heroes[1], tolerance=0.2)
		print(derp)
		self.click_asset(derp, 2, xoffset=20)

	def do_mail(self):
		self.do_steps(
			self.mail,
			delay=1,
			tolerance=0
		)

		self.do_steps(
			self.mail_collect,
			delay=2,
			tolerance=0
		)

		self.do_steps(
			self.gift_collect,
			delay=2,
			tolerance=0.2
		)

		self.escape_back(self.decline, 2)
		self.last_mail_run = self.get_timestamp()

	def do_blitz(self):
		if self.check_cooldown(self.last_blitz_run, self.blitz_cooldown):
			self.do_steps(self.goto_blitz)

			for tier in self.goto_bliz_tier:
				self.find_and_click_asset(tier, tolerance=0.2)
				self.do_steps(self.do_blitz_rounds, loop=True)

	def do_guild_medals(self):
		#goto guild chat
		if self.check_cooldown(self.last_guild_medal_run, self.guild_medal_cooldown):
			self.do_steps(self.guild_chat)
			
			self.do_steps(self.guild_medals_collect)
			self.do_steps(self.guild_medals_help, loop=True, tolerance=0.3, delay=1)
			self.do_steps(self.guild_medals_request, tolerance=0.5, delay=2)
			self.do_steps(self.epic_guild_medals_request, tolerance=0.5, delay=2)

			self.escape_back(self.decline, 2)
			self.last_guild_medal_run = self.get_timestamp()

	def do_expedition(self):
		reward_ready = self.find_asset(None, self.expedition_steps[0], tolerance=0.2)

		if reward_ready or self.check_cooldown(self.last_exped_run, self.exped_cooldown):
			in_exped = self.do_steps([self.expedition_steps[1], self.expedition_steps[2]])
			self.do_steps(self.exped_collect, loop=True, tolerance=0.3, delay=0.5)
			self.do_steps(self.exped_start, loop=True, tolerance=0.3, delay=0.5)

			if in_exped:
				self.escape_back(self.decline, 2)

			self.last_exped_run = self.get_timestamp()
			self.find_and_click_asset(self.screens)
			return True
		return False

	def escape_back(self, back_asset=None, times=1):
		for _ in range(0, times):
			# autopy.key.tap(autopy.key.Code.ESCAPE)
			coords = win32api.MAKELONG(120, 270)
			self.post_button_click(coords,leftbutton=False)
			time.sleep(0.3)

			if self.find_and_click_asset(back_asset, tolerance=0.2):
				return True
		return False

	# def scroll_up_from_asset(assets, distance):
	# 	#toggle click on asset
	# 	#slow move up
	# 	#release click
	# 	return

	def is_out_of_app(self):
		app_screen = self.cta_app

		if self.find_asset(assets=app_screen, tolerance=0.2):
			return True
		return False

	def is_in_main_area(self):
		main_area_markers = self.screens

		if self.find_asset(assets=main_area_markers, tolerance=0.2):
			return True
		return False

	def do_dungeon(self):
		if self.check_cooldown(self.last_dungeon_run, self.dungeon_cooldown):
			new_dungeon_runtime = self.get_timestamp()

			self.do_steps([self.dungeon_steps[0], self.dungeon_steps[1], self.dungeon_steps[2],
						 self.dungeon_steps[3]], tolerance=0.2, delay=0.5)

			decline_found = self.find_and_click_asset(self.decline, tolerance=0.2)

			if self.is_in_main_area():
				self.last_dungeon_run = new_dungeon_runtime
				self.find_and_click_asset(self.screens)
				return False

			if not decline_found:
				time.sleep(0.5)
				victory = False
				while not victory:
					time.sleep(4)
					victory = self.do_dungeon_boss()

			self.last_dungeon_run = new_dungeon_runtime
			self.find_and_click_asset(self.screens)
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

		get_rewards = self.find_and_click_asset(self.dungeon_steps[6], tolerance=0.2)
		if not get_rewards:
			return False
		return True

	def do_math_for_nerds(self):
		stage, screen = self.get_stage_number()

		# print(stage)

		stage_number = float(stage)

		stage_difference = 0
		staging_average = 0
		stage_parsed_correctly = True

		ln = "trouble parsing stage #{}".format(stage_number)
		if self.last_stage_check is not None:
			stage_difference = stage_number - self.last_stage_check

			#you can't generally go back a large number of stages
			if stage_difference > 0 and stage_difference < 300:
				self.stage_reports.append(stage_difference)
				staging_average = round(sum(self.stage_reports) / len(self.stage_reports), 2)
			else:
				stage_number = self.last_stage_check
				stage_parsed_correctly = False
				# self.broken_stages.append(stage_number)

				# if len(self.broken_stages > 1):
				# 	if
				# screen.save("debug/stage{}.png".format(stage_number))

		self.last_stage_check = stage_number

		percent_complete = str(round((stage_number / self.target_stage) * 100, 3))

		f = open("log.txt", "w")
		ln2 = ""
		self.trouble_parsing_stage_count = self.trouble_parsing_stage_count + 1

		if stage_parsed_correctly:
			self.trouble_parsing_stage_count = 0
			ln = ("Percent complete: {}/{} : {}%".format(str(stage_number),
							str(self.target_stage), percent_complete))
			ln2 = ("{} stages since last check, {} avg speed".format(str(stage_difference),
						str(staging_average)))
		else:
			self.escape_back(self.decline)
			time.sleep(1)

		f.write("Python bot for mobile game:\ncrush them all\n{}\n{}\n".format(ln, ln2))
		f.close()

		print(ln, ln2)

		return stage_number

	def do_ascend(self):
		ascended = False
		if self.check_cooldown(self.last_ascend_check, self.ascend_cooldown, log=True):	
			try:
				self.last_ascend_check = self.get_timestamp()
				stage_number = self.do_math_for_nerds()

				if self.trouble_parsing_stage_count > self.max_trouble_parsing_count:
					self.trouble_parsing_stage_count = 0
					self.restart_app()
					self.try_ascend()

				if stage_number >= self.target_stage:
					self.try_ascend()
				
			except Exception as e:
				print(e)
		return ascended

	def try_ascend(self):
		ascended = False
		if self.find_and_click_asset(self.ascend_steps[0], 3, tolerance=0.2, persistent=True):
			if self.find_and_click_asset(self.ascend_steps[1]):
				self.find_and_click_asset(self.ascend_steps[2], tolerance=0.2)
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
		return ascended

	def do_speedad(self):
		speedad_ready = self.find_and_click_asset(self.speedad_steps[0], tolerance=0.2)

		if speedad_ready:
			ad_launched = self.launch_ad(self.speedad_steps[1])
		
			if ad_launched:
				return True
		
		return False

	def do_goldad(self):
		if self.check_cooldown(self.last_goldad_run, self.goldad_cooldown):
			on_shop = self.find_and_click_asset(self.goldad_steps[0])

			if on_shop:
				ad_complete = self.launch_ad(self.goldad_steps[1])
				
				if ad_complete:
					self.find_and_click_asset(self.goldad_steps[2]) #escape the last step
					self.switch_screens(True) #no point to stay on the shop page
				
		self.last_goldad_run = self.get_timestamp()


	def launch_ad(self, ad_asset, timeout=7):
		ad_confirm = self.find_and_click_asset(ad_asset, tolerance=0.2, persistent=True)
		if ad_confirm:
			time.sleep(timeout)

			#check to see if the ad launched properly (look for ascend?)
			if self.is_in_main_area():
				return False
			
			#check to see if we crashed
			if self.find_asset(None, self.cta_app, tolerance=0.2):
				self.restart_app()
				return False

			ad_complete = False
			adtimeout = 60
			adstart = self.get_timestamp()
			while not ad_complete :
				if self.check_cooldown(adstart, adtimeout):
					self.find_and_click_asset(self.ad_exit, tolerance=0)

					ad_complete = self.check_if_ad_is_done(15)
					if ad_complete:
						self.escape_back(self.decline, 3)
						return True

					print("restarting app")
					self.restart_app()
					return False
				ad_complete = self.check_if_ad_is_done(7)

				if ad_complete:
					self.escape_back(self.decline, 3)
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
			app_opened = self.find_and_click_asset(self.cta_app, tolerance=0.2)
			time.sleep(1)

		self.clear_menus()		
		
		print ("app opened")

	def clear_menus(self):
		menus_showing = True
		is_in_main_area = False
		while menus_showing or not is_in_main_area:
			print("looking to clear menus")
			is_in_main_area = self.is_in_main_area()
			menus_showing = self.find_and_click_asset(self.escape_menus, tolerance=0.2)
			time.sleep(1)
			print("Menu found", menus_showing and not is_in_main_area)
			if not menus_showing:
				self.escape_back(self.decline, 2)
	
	def exit_app(self):
		while not self.is_out_of_app():
			print("tryin ta leave app")
			self.find_and_click_asset(self.os_error, tolerance=0.2)
			time.sleep(2)
			autopy.key.tap(autopy.key.Code.PAGE_UP)
			time.sleep(5) #takes a while for the X to appear
			self.find_and_click_asset(self.get_bitmap("assets/gamequit.png"), tolerance=0.2)
			time.sleep(10)
		
	def check_if_ad_is_done(self, timeout):
		self.find_and_click_asset(self.ad_exit, tolerance=0)
		resume_found = self.escape_back(self.resume_button)

		if resume_found:
			time.sleep(timeout)
			return False
		else:
			return self.is_in_main_area()
			# screen = self.refresh_screen()
			# ad_complete_needle = get_bitmap('assets/screen_battle.png')
			# ad_complete = find_asset(screen, ad_complete_needle, tolerance=0.2)
			# if ad_complete:
			# 	return True
			# else:
			# 	return False

	def do_chests(self, screen=None, do_gold_chests=True):
		found_chest = False
		if screen is None:
			screen = self.refresh_screen(3)
		found_chest = self.find_and_click_asset(self.brown_chests, tolerance=0.3, screen=screen, yoffset=125)

		if not found_chest and do_gold_chests:
			gold_chest_clicked = self.find_and_click_asset(self.gold_chests[0], tolerance=0.3, screen=screen, yoffset=125)

			if gold_chest_clicked:
				time.sleep(0.2)
				if self.launch_ad(self.gold_chests[1]):
					time.sleep(1)
					self.find_and_click_asset(self.gold_chests[2])

	def switch_screens(self, force_switch=False):
		if force_switch or self.check_cooldown(self.last_screen_switch, self.screen_switch_cooldown):
			self.find_and_click_asset(self.screens)
			self.last_screen_switch = self.get_timestamp()
			return True
		return False

	def do_weapons(self, tolerance=0):
		screen = self.refresh_screen(3)
		self.do_chests(screen)
		used_weapon = False
		if self.check_cooldown(self.last_weapon_run, self.weapon_cooldown):
			if self.do_edge(screen):
				# screen = self.refresh_screen(3)
				if self.find_and_click_asset(self.weapons, tolerance=0.3, screen=screen, yoffset=125):
					self.last_weapon_run = self.get_timestamp()
					used_weapon = True
				# self.do_chests(screen)
		return used_weapon

	def do_edge(self, screen=None):
		if screen is None:
			screen = self.refresh_screen(3)

		if self.edge_loc is None:
			self.switch_screens(True)
			self.edge_loc = self.find_asset(screen, self.edge)
		
		edge_found = self.find_and_click_asset(self.edge, yoffset=95, screen=screen)

		if not edge_found:
			self.edge_loc = None

		return edge_found

	def do_functions(self, other_functions_done=True):
		if not other_functions_done or self.check_cooldown(self.last_function_run, self.functions_cooldown):
			self.find_and_click_asset(self.collections, tolerance=0.2)
			self.find_and_click_asset(self.functions, 3, tolerance=0.2)
			self.do_chests()
			self.do_steps(self.escape_menus, 1, True)
			
			self.last_function_run = self.get_timestamp()
			
			return True
		return False

	def get_stage_number(self, imPath=None, output=False, threshold=220):
		screen = None
		if imPath is None:
			screen = self.refresh_screen(4)
			screen.save("stage.png")
			imPath = "stage.png"


		pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
		im = Image.open(imPath)

		im = im.convert("RGBA")
		newimdata = []
		datas = im.getdata()

		for item in datas:
			if item[0] > threshold or item[1] > threshold or item[2] > threshold:
				newimdata.append((0,0,0))
			else:
				newimdata.append((255, 255, 255))
		im.putdata(newimdata)

		# im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
		# enhancer = ImageEnhance.Contrast(im)
		# im = enhancer.enhance(5)

		im = im.convert('1')

		text = pytesseract.image_to_string(im,config='-c tessedit_char_whitelist=0123456789 --psm 6', lang='eng')

		# if output:
		# 	im.save("{}.{}.out.png".format(imPath,text))

		return text, screen

	def do_steps(self, steps, delay=0.5, loop=False, tolerance=0.2):
		completed_once = False
		clicked_step = True
		while clicked_step:
			for step in steps:
				step_done = self.find_and_click_asset(step, tolerance=tolerance)

				if not step_done:
					clicked_step = False
					continue
				time.sleep(delay)
			if step_done:
				completed_once = True
				if not loop:
					break
		return completed_once

	def find_and_click_asset(self, assets, click_x_times=1, xoffset=0, yoffset=0,
							tolerance=0, persistent=False, sleep_after_click=0.2,
							screen=None, toggle_state=0):
		clicked = False
		click_attempted = False
		while not clicked:
			if screen is None:
				screen = self.refresh_screen()
			asset = self.find_asset(screen, assets, tolerance)
			if asset:
				self.click_asset(asset, click_x_times, xoffset, yoffset, sleep_after_click, toggle_state)
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

	def find_asset(self, screen=None, assets=None, tolerance=0):
		if assets is None:
			return None

		if screen is None:
			screen = self.refresh_screen()

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

	def find_every_asset(self, assets, screen=None, tolerance=0):
		found_assets = []

		if assets is None:
			return []

		if screen is None:
			screen = self.refresh_screen()

		if isinstance(assets, list):
			for asset in assets:
				found_asset = screen.find_every_bitmap(asset, tolerance=tolerance)
				if found_asset:
					found_assets.append(found_asset)
		else:
			found_assets = screen.find_every_bitmap(assets, tolerance=tolerance)

		return found_assets

	def click_asset(self, found_asset, count=1, xoffset=0, yoffset=0,
					 sleep_after_click=0.1, toggle_state=0):
		# autopy.mouse.move(found_asset[0]+xoffset, found_asset[1]+yoffset)
		coords = win32api.MAKELONG(int(found_asset[0]+xoffset), int(found_asset[1]+yoffset))

		for _ in range(0,count):
			self.post_button_click(coords)
			# if toggle_state == 0:
				# autopy.mouse.click()
			# elif toggle_state == 1:
				# autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
			# elif toggle_state == 2:
				# autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
			time.sleep(sleep_after_click)

	def get_bitmap(self, file):
		return autopy.bitmap.Bitmap.open(file)

	def refresh_screen(self, size=1):
		x,y = self.get_window_screenshot(self.window)
		# screenshot.save("test.png")
		# screen = autopy.bitmap.Bitmap.open("test.png")

		# screen = None
		crop = ((x,y), (390,727))

		if size == 1:
			crop = ((x,y), (390,727))
		elif size == 2:
			crop = ((x,y), (390,350))
			# screen = autopy.bitmap.capture_screen(((0,0), (390,350)))
		elif size == 3:
			crop = ((x,y+125), (390,225))
		else:
			crop = ((x+197,y+30), (40,30))

		# if screen:
		# 	screen = screen.cropped(crop)
		# else:
		screen = autopy.bitmap.capture_screen(crop)

		return screen

	def get_window(self, name):
		return win32gui.FindWindow(None, name)

	def post_button_click(self, coords=1000, stime=0.1, leftbutton=True):
		win32gui.PostMessage(self.window, win32con.WM_MOUSEMOVE, 0, coords)
		if leftbutton:
			win32gui.PostMessage(self.window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, coords)
		else:
			win32gui.PostMessage(self.window, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, coords)			
		time.sleep(stime)
		self.move_mouse(self.window, coords)

	def move_mouse(self, hwnd, coords):
	    win32gui.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 0, coords)

	def get_window_screenshot(self, hwnd, maxheight=-1):
		left, top, right, bot = win32gui.GetClientRect(hwnd)

		return left, top
		# if maxheight > 0:
		# 	h = maxheight

		# hwndDC = win32gui.GetWindowDC(hwnd)
		# mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
		# saveDC = mfcDC.CreateCompatibleDC()
		# saveBitMap = win32ui.CreateBitmap()
		# saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
		# saveDC.SelectObject(saveBitMap)
		# result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

		# bmpinfo = saveBitMap.GetInfo()
		# bmpstr = saveBitMap.GetBitmapBits(True)

		# return Image.frombuffer(
		# 	'RGB',
		# 	(bmpinfo['bmWidth'], bmpinfo['bmHeight']),
		# 	bmpstr, 'raw', 'BGRX', 0, 1)

	def check_cooldown(self, last_use, cooldown, log=False):
		start = self.get_timestamp()
		is_expired = False
		if not last_use:
			return True
		timer = self.get_timestamp() - last_use
		seconds = timer

		# if log:
		# 	next_asc_minutes = round((cooldown - seconds) / 60, 2)
		# 	print(str(next_asc_minutes))

		if seconds > cooldown:
			is_expired = True
		# self.check_perf("cooldown", start, False)
		return is_expired

if __name__ == '__main__':
	bot = Bot()
	P = PlayerKeyboard(bot)
	P.start()
	bot.main()