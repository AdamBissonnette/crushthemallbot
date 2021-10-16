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
		self.logs = []
		self.window = self.get_window('NoxPlayer')

		self.screens = [
			self.get_bitmap('assets/screen_heroes.png'),
			self.get_bitmap('assets/screen_village.png'),
		]
		self.brown_chests = [
			# self.get_bi('assets/chest_bull1.png'),
			# self.get_bitmap('assets/chest_bull2.png'),
			# self.get_bitmaptmap('assets/chest_bull3.png'),
			# self.get_bitmap('assets/chest_egg1.png'),
			# self.get_bitmap('assets/chest_egg2.png'),
			# self.get_bitmap('assets/chest_egg3.png'),
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
		self.get_reward = [
			self.get_bitmap('assets/reward_get.png')
		]
		self.weapons = [
			self.get_bitmap('assets/weapon_light.png'),
			self.get_bitmap('assets/weapon_fire.png'),
			self.get_bitmap('assets/weapon_earth.png'),
			self.get_bitmap('assets/weapon_swords.png'),
			self.get_bitmap('assets/weapon_dark.png'),
		]

		self.decline = self.get_bitmap('assets/decline.png')
		self.okay = self.get_bitmap('assets/okay.png')
		self.ok = self.get_bitmap('assets/ok.png')
		self.cta_app = self.get_bitmap('assets/crush_them_all_app.png')
		self.os_error = self.get_bitmap('assets/crash_game_stopped.png')
		self.signed_out = [self.get_bitmap('assets/app_signed_out.png'), self.get_bitmap('assets/app_signed_out2.png')]
		self.screen_saver = self.get_bitmap('assets/screen_saver2.png')

		self.escape_menus = [
			self.cta_app,
			self.decline,
			self.okay,
			self.ok,
			self.get_bitmap('assets/chest_gold_step3.png'),
			self.get_bitmap('assets/away_okay.png'),
			self.get_bitmap('assets/X.png'),
			self.get_bitmap('assets/X2.png'),
			self.get_bitmap('assets/modal_pack_x.png'),
			self.os_error,
			self.screen_saver,
			self.get_bitmap('assets/game_still_running_okay2.png'),
			self.get_bitmap('assets/reward_get.png')
		]
		self.upgrade_villages = [
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
			self.get_bitmap('assets/ascend_step1.png', False),
			[
				# self.get_bitmap('assets/ascend_step2_double.png'),
				self.get_bitmap('assets/ascend_step2.png', False),
			],
			self.get_bitmap('assets/ascend_accept.png', False),
			self.get_bitmap('assets/ascend_step4.png', False),
			self.get_bitmap('assets/ascend_step5.png', False)
		]

		self.dungeon_steps = [
			self.get_bitmap('assets/screen_battle.png', False),
			[
				self.get_bitmap('assets/dungeon_step1.png', False),
				# self.get_bitmap('assets/dungeon_step1_event.png'),
			],
			# self.get_bitmap('assets/dungeon_step2.png'),
			[
				# self.get_bitmap('assets/dungeon_earth.png'),
				# self.get_bitmap('assets/dungeon_fire.png'),
				# self.get_bitmap('assets/dungeon_dark.png'),
				# self.get_bitmap('assets/dungeon_step2_event.png'),
				self.get_bitmap('assets/dungeon_step2.png', False),
				self.get_bitmap('assets/dungeon_step2_alt.png', False),
				self.get_bitmap('assets/dungeon_enter.png', False),
			], #top or mid or enter button dungeon
			[
				self.get_bitmap('assets/dungeon_step3.png', False), #highest rank dungeon
				self.get_bitmap('assets/dungeon_step3_2ndlast.png', False), #highest rank dungeon
				self.get_bitmap('assets/dungeon_step3_last2.png', False), #highest rank dungeon
				self.get_bitmap('assets/dungeon_step3_last3.png', False), #highest rank dungeon
				# self.get_bitmap('assets/dungeon_step3_event.png'),
			],
			self.get_bitmap('assets/decline.png'),
			self.get_bitmap('assets/dungeon_edge.png'),
			self.get_bitmap('assets/dungeon_okay.png'),
		]

		self.reward_ready = [self.get_bitmap('assets/exped_step0_reward_ready.png', False)]

		self.expedition_steps = [
			self.get_bitmap('assets/screen_battle.png', False),
			self.get_bitmap('assets/exped_step1.png', False),
		]

		self.exped_start = [
			[self.get_bitmap('assets/exped_step2_run.png', False),
			self.get_bitmap('assets/exped_step2_run2.png', False)],
			self.get_bitmap('assets/exped_step3_autofill.png', False),
			self.get_bitmap('assets/exped_step4_start.png', False),
		]

		self.exped_collect = [
			[self.get_bitmap('assets/exped_step5_collect.png', False),
			self.get_bitmap('assets/exped_step5_collect2.png', False),
			self.get_bitmap('assets/exped_step5_collect3.png', False),
			self.get_bitmap('assets/exped_step5_collect4.png', False),
			],
			self.get_bitmap('assets/exped_step6_confirm.png', False),
		]

		self.exped_claim_all = [
			self.get_bitmap('assets/exped_claim_all.png')
		]

		self.exped_okay = [
			self.get_bitmap('assets/exped_step6_confirm.png')
		]

		self.exped_send_all = [
			self.get_bitmap('assets/exped_send_all.png')
		]

		self.guild_chat = [
			self.get_bitmap('assets/screen_guild.png'),
			self.get_bitmap('assets/guild_chat.png'),
		]

		self.guild_medals_collect = [
			self.get_bitmap('assets/guild_medals_collect.png'),
			self.get_bitmap('assets/guild_medals_collect2.png'),
		]

		self.guild_medals_help = [
			self.get_bitmap('assets/guild_medals_help.png'),
			self.get_bitmap('assets/guild_medals_help2.png')
		]

		self.guild_medals_request = [
			self.get_bitmap('assets/guild_medal_request.png'),
			self.get_bitmap('assets/guild_medal.png'),
			self.get_bitmap('assets/guild_medal_request3.png'),
		]

		self.epic_guild_medals_request = [
			self.get_bitmap('assets/guild_medal_request2.png'),
			self.get_bitmap('assets/guild_medal2.png'), 
			self.get_bitmap('assets/guild_medal_request3A.png'),
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
				self.get_bitmap("assets/ad_resume.png", False), 
				self.get_bitmap("assets/ad_resume2.png", False),
				self.get_bitmap("assets/ad_resume3.png", False),
				self.get_bitmap("assets/ad_resume4.png", False),
				self.get_bitmap("assets/ad_resume5.png", False),
				self.get_bitmap("assets/ad_resume6.png", False),
				self.get_bitmap("assets/ad_resume7.png", False),
				self.get_bitmap("assets/ad_resume8.png", False),
				]

		self.gs_exit = [
			self.get_bitmap('assets/ad_exit1.png.gs.png', False),
			self.get_bitmap('assets/ad_exit2.png.gs.png', False),
			self.get_bitmap('assets/ad_exit3.png.gs.png', False),
			self.get_bitmap('assets/ad_exit4.png.gs.png', False),
			self.get_bitmap('assets/ad_exit5.png.gs.png', False),
			self.get_bitmap('assets/ad_exit6.png.gs.png', False),
			self.get_bitmap('assets/ad_exit7.png.gs.png', False),
			self.get_bitmap('assets/ad_exit12.png.gs.png', False),
			self.get_bitmap('assets/ad_exit13.png.gs.png', False),
			self.get_bitmap('assets/ad_exit14.png.gs.png', False),
			self.get_bitmap('assets/ad_exit15.png.gs.png', False),
			self.get_bitmap('assets/ad_exit16.png.gs.png', False),
			self.get_bitmap('assets/ad_exit17.png.gs.png', False),
		]
		self.ad_exit = [
			self.get_bitmap('assets/ad_exit0.png', False),
			self.get_bitmap('assets/ad_exit18.png', False),
			self.get_bitmap('assets/ad_exit19.png', False),
			self.get_bitmap('assets/ad_exit1.png', False),
			self.get_bitmap('assets/ad_exit2.png', False),
			self.get_bitmap('assets/ad_exit3.png', False),
			self.get_bitmap('assets/ad_exit4.png', False),
			self.get_bitmap('assets/ad_exit5.png', False),
			self.get_bitmap('assets/ad_exit6.png', False),
			self.get_bitmap('assets/ad_exit7.png', False),
			self.get_bitmap('assets/ad_exit12.png', False),
			self.get_bitmap('assets/ad_exit13.png', False),
			self.get_bitmap('assets/ad_exit14.png', False),
			self.get_bitmap('assets/ad_exit15.png', False),
			self.get_bitmap('assets/ad_exit16.png', False),
			self.get_bitmap('assets/ad_exit17.png', False),
			self.get_bitmap('assets/ad_retry.png', False),
		]

		self.ad_close = [
			self.get_bitmap('assets/ad_close.png', False),			
			self.get_bitmap('assets/ad_close2.png', False),			
			self.get_bitmap('assets/ad_close3.png', False),			
			self.get_bitmap('assets/ad_close4.png', False),			
			self.get_bitmap('assets/ad_close5.png', False),			
			self.get_bitmap('assets/ad_close6.png', False),			
			self.get_bitmap('assets/ad_close7.png', False),			
			self.get_bitmap('assets/ad_close8.png', False),			
			self.get_bitmap('assets/ad_close9.png', False),			
		]

		self.goldad_steps = [
			self.get_bitmap('assets/screen_shop.png'),
			[
				self.get_bitmap('assets/goldad_step1.png'),
				self.get_bitmap('assets/goldad_step1_alt.png'),
				self.get_bitmap('assets/goldad_step1_alt2.png'),
				self.get_bitmap('assets/goldad_step1_alt3.png'),
			],
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

		self.slay_bosses = [
			self.get_bitmap('assets/screen_guild.png'),
			self.get_bitmap('assets/slay_bosses_step_1.png'), #enter bosses
			[self.get_bitmap('assets/slay_bosses_step_2.png'), #click top battle
			self.get_bitmap('assets/slay_bosses_step_2A.png')] #click top battle
		]

		self.slay_bosses_quick = [
			self.get_bitmap('assets/slay_bosses_step_3.png'),
			self.get_bitmap('assets/slay_bosses_step_4.png'),
		]

		self.slay_bosses_slow = [
			[self.get_bitmap('assets/slay_bosses_step_3A.png'), 
			self.get_bitmap('assets/slay_bosses_step_3AA.png')] 
		]

	def stop(self):
		self.stopping = True

	def grayscale_image(self, imPath, threshold = 200):
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

		im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
		enhancer = ImageEnhance.Contrast(im)
		im = enhancer.enhance(5)

		im = im.convert('1')
		return im

	def gs_ad_exits(self):
		for exit in self.ad_exit:
			filename = exit["name"]
			gs_exit = self.grayscale_image(filename)
			gs_exit.save(filename + '.gs.png')

	def convert_debug_ads(self):
		from os import walk

		f = []
		for (dirpath, dirnames, filenames) in walk('./ads_debug'):
			f.extend(filenames)
			break
		
		for name in filenames:
			im = self.grayscale_image('ads_debug/'+name)
			im.save('converted_ads/'+name)

	def test_debug_ads_images(self, dir='converted_ads', assets=None):
		if not assets:
			assets = self.gs_exit

		start = time.perf_counter()
		from os import walk

		f = []
		for (dirpath, dirnames, filenames) in walk('./' + dir):
			f.extend(filenames)
			break
		
		for name in filenames:
			# if "2598" in name:
			screen = self.get_bitmap(dir + '/'+name)
			found = False

			for asset in assets:
				found = self.find_asset(screen["data"], asset, tolerance=0)
				if found:
					print ("{} {}".format(screen["name"], asset["name"]), found)
					break
			if not found:
				print("{} no exit found".format(screen["name"]))

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

					# self.print_log(name, text, text in name and len(text) > 1)

		self.print_log("{} {} {} {} {}".format(threshold, x, i, round((x/i) *100, 2), time.perf_counter() - start))
			
			# if i >= 10:
			# 	return

	def main(self):
		# self.test_debug_ads_images('ads_debug', self.ad_exit)
		# return

		# self.test_debug_ads_images()
		# return

		# self.convert_debug_ads()
		# return

		# self.gs_ad_exits()
		# return

		screen = self.refresh_screen()
		screen.save("screen.png")
		
		# print(self.find_and_click_asset(self.dungeon_steps[2], tolerance=0.3))

		# return
		self.last_stage_check = None
		self.last_stack_check_timestamp = None
		self.trouble_parsing_stage_count = 0
		self.max_trouble_parsing_count = 5
		self.stage_reports = []
		self.target_stage = 8415
		self.ascend_cooldown = 60
		self.dungeon_cooldown = 900
		self.exped_cooldown = 600
		self.weapon_cooldown = 1 #0.65
		self.blitz_cooldown = 6000
		self.screen_switch_cooldown = 120
		self.functions_cooldown = 60
		self.guild_medal_cooldown = 915
		self.goldad_cooldown = 1000
		self.signed_out_check_cooldown = 30
		self.slay_bosses_cooldown = 600
		self.do_gold_chests = True

		self.last_guild_medal_run = self.get_timestamp()
		self.last_dungeon_run = self.get_timestamp()
		self.last_exped_run = self.get_timestamp()
		self.last_weapon_run = None
		self.last_goldad_run = None #self.get_timestamp()
		self.last_ascend_check = None #self.get_timestamp()
		self.last_screen_switch = None #self.get_timestamp()
		self.last_function_run = self.get_timestamp()
		self.last_signed_out_check = None
		self.last_blitz_run = None
		self.last_slay_bosses_run = None
		self.stopping = False

		self.switch_screens()
		# self.do_guild_medals()
		# self.find_and_click_asset(self.ad_exit, tolerance=0.2)
		# return

		while not self.stopping:
			# self.last_stage_check = 1
			# self.do_mail()
			# return
			# start = self.get_timestamp()
			self.check_for_sign_out()
			# self.check_perf("routines ", start)
			# self.do_blitz()
			# return
			self.do_edge()
			self.do_ascend()
			self.do_speedad()
			# self.do_goldad() # Broken
			self.do_dungeon()
			self.do_expedition()
			self.do_guild_medals()
			# self.do_slay_bosses()
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
			# weapons_done = self.do_weapons()
			self.do_weapons()
			# self.check_perf("weapons", start)

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
			self.print_log("{} {} {} {}".format(note, curTime, seconds, (curTime-seconds)*1000))

	def check_for_sign_out(self):
		if self.check_cooldown(self.last_signed_out_check, self.signed_out_check_cooldown):
			signed_out = self.find_asset(None, self.signed_out, tolerance=0.2)
			if signed_out:
				self.print_log("signed out of app - restarting")
				#wait 15 minutes before re-opening the app
				self.restart_app(900)
				self.last_signed_out_check = self.get_timestamp()

	def max_level_heroes(self):
		level_up = self.find_asset(None, self.upgrade_heroes[0], tolerance=0.2)
		self.click_asset(level_up, toggle_state=1, sleep_after_click=1, xoffset=30)
		self.click_asset(level_up, toggle_state=2, sleep_after_click=1,
					xoffset=-20, yoffset=-20)
		derp = self.find_asset(None, self.upgrade_heroes[1], tolerance=0.2)
		self.print_log(derp)
		self.click_asset(derp, 2, xoffset=20)

	def do_slay_bosses(self):
		if self.check_cooldown(self.last_slay_bosses_run, self.slay_bosses_cooldown):
			self.do_steps(self.slay_bosses, delay=1)

			if self.find_asset(None, self.slay_bosses_quick[0], tolerance=0.2):
				self.do_steps(self.slay_bosses_quick, delay=0.5)
			else:
				self.do_steps(self.slay_bosses_slow, delay=0.5)
			
			self.print_log("starting loop")
			time.sleep(3)
			found_okay = self.find_asset(None, self.okay, tolerance=0.3)
			while not found_okay:
				self.print_log("in loop")
				self.escape_back(self.decline, 2)
				time.sleep(2)
			
			self.print_log("escaping")
			time.sleep(2)
			self.escape_back(self.decline, times=3)
			self.last_slay_bosses_run = self.get_timestamp()

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

	def do_guild_medals(self, help=True):
		#goto guild chat
		if self.check_cooldown(self.last_guild_medal_run, self.guild_medal_cooldown):
			self.do_steps(self.guild_chat)
			time.sleep(1)
			
			self.do_steps(self.guild_medals_collect, tolerance=0.3)
			time.sleep(3)
			if help:
				self.do_steps(self.guild_medals_help, loop=True, tolerance=0.3, delay=1)

			if not self.do_steps(self.epic_guild_medals_request, tolerance=0.3, delay=1):
				self.do_steps(self.guild_medals_request, tolerance=0.2, delay=2)

			self.escape_back(self.decline, 2)
			self.last_guild_medal_run = self.get_timestamp()

	def do_expedition(self):
		reward_ready = self.find_asset(None, self.reward_ready, tolerance=0.2)

		if reward_ready or self.check_cooldown(self.last_exped_run, self.exped_cooldown):
			in_exped = self.do_steps(self.expedition_steps)
			# self.do_steps(self.exped_collect, loop=True, tolerance=0.3, delay=0.5)
			# self.do_steps(self.exped_start, loop=True, tolerance=0.3, delay=0.5)
			self.do_steps(self.exped_claim_all, tolerance=0.3, delay=0.5)
			self.do_steps(self.exped_okay, tolerance=0.3, delay=0.5, loop=True)
			self.do_steps(self.exped_send_all, tolerance=0.3, delay=0.5)

			if in_exped:
				self.escape_back(self.decline, 2)

			self.last_exped_run = self.get_timestamp()
			self.find_and_click_asset(self.screens)
			return True
		return False

	def click_back(self):
		coords = win32api.MAKELONG(120, 270)
		self.post_button_click(coords,key=3)

	def escape_back(self, back_asset=None, times=1, tolerance=0.2):
		for _ in range(0, times):
			# autopy.key.tap(autopy.key.Code.ESCAPE)
			self.click_back()
			time.sleep(0.3)

			if self.find_and_click_asset(back_asset, tolerance=tolerance):
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

			if self.do_steps([self.dungeon_steps[0], self.dungeon_steps[1], self.dungeon_steps[2]], tolerance=0.2, delay=2):
				time.sleep(3)
				self.find_and_click_asset(self.dungeon_steps[3], tolerance=0.2)

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
			self.switch_screens(False)
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

	def print_log(self, text, timestamp=None):
		# if timestamp:
		# 	timestamp = datetime.now().strftime("%H:%M:%S")
		print("{}: {}".format(datetime.now().strftime("%H:%M:%S"), text))

	def do_math_for_nerds(self):
		# self.last_stage_check_time = self.stage_check_time
		# stage_check_time = self.get_timestamp()
		stage, screen = self.get_stage_number()		

		# self.print_log(stage)

		stage_number = float(stage)
		stage_check_time = self.get_timestamp()

		stage_difference = 0
		staging_average = 0
		# time_difference = 0
		stage_parsed_correctly = True

		
		ln = "{}, trouble parsing stage #{}".format(datetime.now().strftime("%H:%M:%S"), stage_number)
		if self.last_stage_check is not None:
			stage_difference = stage_number - self.last_stage_check

			#you can't generally go back a large number of stages
			if stage_difference > 0 and stage_difference < 300:
				# self.last_valid_stage_check_time = self.stage_check_time
				self.stage_reports.append(stage_difference)
				# time_difference = self.stage_check_time - self.last_stage_check_time
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

		# f = open("log.txt", "w")
		ln2 = ""
		self.trouble_parsing_stage_count = self.trouble_parsing_stage_count + 1

		if stage_parsed_correctly:
			self.trouble_parsing_stage_count = 0
			# log = {}
			
			ln = ("Percent complete: {}/{} : {}%".format(str(stage_number),
							str(self.target_stage), percent_complete))
			ln2 = ("{} stages since last check, {} avg speed".format(str(stage_difference),
						str(staging_average)))
			self.current_stage = stage_number

			# if len(self.logs) > 0:
			# 	last_log = self.logs[len(self.logs - 1)]
			# 	minute_difference = (stage_check_time - last_log["time"])/60
			# 	stages_per_minute = stage_difference/minute_difference
			# 	ln3 = ("{} stages per minute".format(stages_per_minute))

			# 	log["stage_number"] = str(stage_number)
			# 	log["percent_complete"] = percent_complete
			# 	log["stage_difference"] = str(stage_difference)
			# 	log["stage_average"] = str(staging_average)
			# 	log["target_stage"] = str(self.target_stage)
			# 	log["time"] = stage_check_time
			# 	log["stages_per_minute"] = stages_per_minute
			# 	self.logs.append(log)
		else:
			self.escape_back(self.decline)
			time.sleep(1)

		# f.write("Python macro for mobile game:\ncrush them all\n{}\n{}\n".format(ln, ln2))
		# f.close()

		self.print_log(ln + " " + ln2, timestamp=stage_check_time)

		return stage_number

	def do_ascend(self):
		ascended = False
		if self.check_cooldown(self.last_ascend_check, self.ascend_cooldown, log=True):	
			try:
				self.last_ascend_check = self.get_timestamp()
				self.stage_number = self.do_math_for_nerds()

				if self.trouble_parsing_stage_count > self.max_trouble_parsing_count:
					self.print_log("resetting stage number")
					self.stage_number = None
					self.last_stage_check = None
					# if we failed to parse the stage check again sooner
					self.last_ascend_check = self.last_ascend_check - self.ascend_cooldown/2
					if self.trouble_parsing_stage_count > (self.max_trouble_parsing_count * 2):
						self.restart_app()
						self.escape_back(self.decline, 2)
						# self.try_ascend()
					return False
					# self.restart_app()
					# self.try_ascend()

				if self.stage_number >= self.target_stage and self.stage_number <= (self.target_stage + 300):
					self.try_ascend()
				# if we're close to our target stage then check more
				elif (self.stage_number + 30) >= self.target_stage:
					self.last_ascend_check = self.last_ascend_check - self.ascend_cooldown/2
				
				
			except Exception as e:
				self.print_log("{} {}".format(datetime.now().strftime("%H:%M:%S"), e))
				self.escape_back(self.decline, 3)

		return ascended

	def try_ascend(self):
		ascended = False
		if self.find_and_click_asset(self.ascend_steps[0], 3, tolerance=0.2):
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
				self.stage_number = None
				ascended = True
			else:
				self.escape_back(self.decline, 3)
		return ascended

	def do_speedad(self):
		speedad_ready = self.find_and_click_asset(self.speedad_steps[0], tolerance=0.2)

		if speedad_ready:
			ad_launched = self.launch_ad(self.speedad_steps[1])
		
			if ad_launched:
				self.print_log("Speed ad run")
				return True
		
		return False

	def do_goldad(self):
		if self.check_cooldown(self.last_goldad_run, self.goldad_cooldown):
			on_shop = self.find_and_click_asset(self.goldad_steps[0])
			time.sleep(2)

			if on_shop:
				ad_complete = self.launch_ad(self.goldad_steps[1])
				
				if ad_complete:
					self.find_and_click_asset(self.goldad_steps[2]) #escape the last step
					self.switch_screens(True) #no point to stay on the shop page
					self.print_log("gold ad run")
				
				self.last_goldad_run = self.get_timestamp()


	def launch_ad(self, ad_asset, timeout=7):
		ad_confirm = self.find_and_click_asset(ad_asset, tolerance=0.3, persistent=True)
		if ad_confirm:
			time.sleep(0.5)
			reward_found = self.find_and_click_asset(self.get_reward, tolerance=0.2)
			if reward_found:
				return True

			time.sleep(timeout)

			#check to see if the ad launched properly (look for ascend?)
			if self.is_in_main_area():
				return False
			
			#check to see if we crashed
			if self.find_asset(None, self.cta_app, tolerance=0.2):
				self.restart_app()
				return False

			ad_complete = False
			ad_timeout = timeout
			adcrash_timeout = 30
			adstart = self.get_timestamp()
			iteration = 0
			while not ad_complete:
				iteration += 1
				# self.print_log("starting loop")
				# if self.check_cooldown(adstart, adcrash_timeout):
				# 	self.print_log("restart app")
				# 	self.restart_app()
				# 	return False
				ad_complete = self.check_if_ad_is_done(ad_timeout, self.check_cooldown(adstart, adcrash_timeout), iteration)

			#ad is now complete
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
			self.print_log("tryin ta open app")
			app_opened = self.find_and_click_asset(self.cta_app, tolerance=0.2)
			time.sleep(1)

		self.clear_menus()
		self.switch_screens()
		
		self.print_log ("app opened")

	def clear_menus(self):
		menus_showing = True
		is_in_main_area = False
		while menus_showing or not is_in_main_area:
			self.print_log("looking to clear menus")
			is_in_main_area = self.is_in_main_area()
			menus_showing = self.find_and_click_asset(self.escape_menus, tolerance=0.3)
			time.sleep(1)
			self.print_log("Menu found {}".format(menus_showing and not is_in_main_area))
			if not menus_showing:
				self.escape_back(self.decline, 2)
	
	def exit_app(self):
		while not self.is_out_of_app():
			self.print_log("tryin ta leave app")
			self.find_and_click_asset(self.os_error, tolerance=0.2)
			time.sleep(2)
			self.print_log("page up press")
			autopy.mouse.move(0, 0)
			autopy.mouse.click()
			time.sleep(1)
			autopy.key.tap(autopy.key.Code.PAGE_UP)
			# coords = win32api.MAKELONG(0, 0)
			#page up
			# self.post_button_click(coords,key=3)
			time.sleep(5) #takes a while for the X to appear
			self.find_and_click_asset(self.get_bitmap("assets/gamequit_x.png"), tolerance=0.2)
			time.sleep(10)
		
	def check_if_ad_is_done(self, timeout, close=False, iteration=0):
		self.print_log("Checking if ad is done #" + str(iteration))

		timestamp = datetime.now().strftime("%H:%M:%S")
		exit_screen = self.refresh_screen(2)
		exit_screen.save('temp.png')
		grayscale_exit = self.grayscale_image('temp.png')
		grayscale_exit.save('temp.gs.png')
		exit_screen = self.get_bitmap('temp.gs.png')

		self.click_back()
		self.click_back()
		exit_found = self.find_and_click_asset(self.gs_exit, screen=exit_screen["data"], tolerance=0.1)
		resume_found = False
		if not exit_found:
			resume_found = self.escape_back(self.resume_button)

		if close:
			self.print_log("executing ad close function")
			
			# screen = self.refresh_screen()
			# screen.save("ads_debug/ad_" + str(self.stage_number) + ".png")

			exit_screen = self.refresh_screen(2)
			exit_screen.save('temp.png')
			grayscale_exit = self.grayscale_image('temp.png')
			grayscale_exit.save('temp.gs.png')
			grayscale_exit.save("converted_ads/" + str(self.stage_number) + "_screen.png")
			exit_screen = self.get_bitmap('temp.gs.png')
			found = self.find_and_click_asset(self.gs_exit, screen=exit_screen["data"], tolerance=0.3)
			# (364.0, 67.0)

			if not found:
				if iteration < 12:
					self.click_asset((364.0, 67.0)) # Guess at the general areas
				else:
					self.click_asset((373.0, 50.0))
			# exit_found = self.escape_back(self.ad_close, 2, tolerance=0.3)
			time.sleep(3)
			if self.is_in_main_area():
				return True
			else:
				self.find_and_click_asset(self.ad_exit, tolerance=0.2)
		# if resume_found:
		# 	time.sleep(timeout)
		# 	return False
		# else:
			# self.print_log("found ad exit {}".format(self.find_and_click_asset(self.ad_exit, tolerance=0)))
		time.sleep(3)
		is_in_main = self.is_in_main_area()
		# if exit_found and not is_in_main:
		# 	exit_screen.save("ads_exits/{}_bad_exit_{}{}".format(timestamp, str(self.stage_number), ".png"))
		
		return is_in_main
			# screen = self.refresh_screen()
			# ad_complete_needle = get_bitmap('assets/screen_battle.png')
			# ad_complete = find_asset(screen, ad_complete_needle, tolerance=0.2)
			# if ad_complete:
			# 	return True
			# else:
			# 	return False

	def do_chests(self, screen=None, do_gold_chests=True):
		# return False
		found_chest = False
		if screen is None:
			screen = self.refresh_screen(3)
		found_chest = self.find_and_click_asset(self.brown_chests, tolerance=0.3, screen=screen, yoffset=125)

		if not found_chest and self.do_gold_chests:
			gold_chest_clicked = self.find_and_click_asset(self.gold_chests[0], tolerance=0.3, screen=screen, yoffset=125)

			if gold_chest_clicked:
				time.sleep(0.2)

				if self.launch_ad(self.gold_chests[1]):
					self.print_log("{} launched gold chest ad".format(datetime.now().strftime("%H:%M:%S")))
					time.sleep(1)
					self.find_and_click_asset(self.gold_chests[2])
					time.sleep(0.5)
					self.clear_menus()

	def switch_screens(self, force_switch=False):
		if force_switch or self.check_cooldown(self.last_screen_switch, self.screen_switch_cooldown):
			self.find_and_click_asset(self.screens, tolerance=0.1)
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
				if self.find_and_click_asset(self.weapons, tolerance=0.1, screen=screen, yoffset=125):
					self.last_weapon_run = self.get_timestamp()
					used_weapon = True
				# self.do_chests(screen)
		return used_weapon

	def do_edge(self, screen=None):
		if self.edge_loc is None:
			self.switch_screens(True)
			time.sleep(2)
			screen = self.refresh_screen(3)
			screen.save("taco.png")
			self.edge_loc = self.find_asset(screen, self.edge, tolerance=0.2)
		
		self.click_asset(self.edge_loc, yoffset=95)
		
		# edge_found = self.find_and_click_asset(self.edge, yoffset=95, screen=screen, tolerance=0.2)

		return self.edge_loc

	def do_functions(self, other_functions_done=True):
		if not other_functions_done or self.check_cooldown(self.last_function_run, self.functions_cooldown):
			self.find_and_click_asset(self.collections, tolerance=0.2)

			self.find_and_click_asset(self.upgrade_villages, 3, tolerance=0.2)

			#don't upgrade heroes until we're over 50% of our target stage
			# if self.stage_number > (self.target_stage / 2):
			# 	self.find_and_click_asset(self.upgrade_heroes, 3, tolerance=0.2)
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

	def find_bitmap(self, screen, bitmap, tolerance):
		found = screen.find_bitmap(bitmap["data"], tolerance)
		if bitmap["debug"]:
			self.print_log("{} found {}".format(bitmap["name"], found))
		
		return found

	def find_asset(self, screen=None, assets=None, tolerance=0):
		if assets is None:
			return None

		if screen is None:
			screen = self.refresh_screen()

		if isinstance(assets, list):
			for asset in assets:
				found_asset = self.find_bitmap(screen, asset, tolerance)
				if found_asset:
					return found_asset
		else:
			found_asset = self.find_bitmap(screen, assets, tolerance)
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

	def get_bitmap(self, file, debug=False):
		return {"name": file, "data": autopy.bitmap.Bitmap.open(file), "debug": debug}

	def persistent_screenshot(self):
		screenshot = None

		while screenshot is None:
			try:
				screenshot = self.get_window_screenshot(self.window)
			except Exception:
				screenshot = None
		return screenshot

	def refresh_screen(self, size=1):
		slow_mode = False
		screen = None
		x = 0
		y = 0

		if slow_mode:
			screenshot = self.persistent_screenshot()
			screenshot.save("test.png")
			screen = autopy.bitmap.Bitmap.open("test.png")
		else:
			x,y = self.get_window_position(self.window)


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

		if screen and slow_mode:
			screen = screen.cropped(crop)
		else:
			screen = autopy.bitmap.capture_screen(crop)

		return screen

	def get_window(self, name):
		return win32gui.FindWindow(None, name)

	def post_button_click(self, coords=1000, stime=0.1, key=1):
		win32gui.PostMessage(self.window, win32con.WM_MOUSEMOVE, 0, coords)
		if key == 1:
			win32gui.PostMessage(self.window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, coords)
			win32gui.PostMessage(self.window, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, coords)
		else:
			win32gui.PostMessage(self.window, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, coords)
			win32gui.PostMessage(self.window, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, coords)
		time.sleep(stime)
		self.move_mouse(self.window, coords)

	def move_mouse(self, hwnd, coords):
	    win32gui.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 0, coords)

	def get_window_position(self, hwnd, maxheight=-1):
		left, top, right, bot = win32gui.GetClientRect(hwnd)
		return left, top

	def get_window_screenshot(self, hwnd, maxheight=-1):
		left, top, right, bot = win32gui.GetClientRect(hwnd)

		w = right - left
		h = bot - top
		if maxheight > 0:
			h = maxheight

		hwndDC = win32gui.GetWindowDC(hwnd)
		mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
		saveDC = mfcDC.CreateCompatibleDC()
		saveBitMap = win32ui.CreateBitmap()
		saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
		saveDC.SelectObject(saveBitMap)
		# result = ctypes.windll.user32.self.Print_logWindow(hwnd, saveDC.GetSafeHdc(), 0)

		bmpinfo = saveBitMap.GetInfo()
		bmpstr = saveBitMap.GetBitmapBits(True)

		return Image.frombuffer(
			'RGB',
			(bmpinfo['bmWidth'], bmpinfo['bmHeight']),
			bmpstr, 'raw', 'BGRX', 0, 1)

	def check_cooldown(self, last_use, cooldown, log=False):
		# start = self.get_timestamp()
		is_expired = False
		if not last_use:
			return True
		timer = self.get_timestamp() - last_use
		seconds = timer

		# if log:
		# 	next_asc_minutes = round((cooldown - seconds) / 60, 2)
		# 	self.print_log(str(next_asc_minutes))

		if seconds > cooldown:
			is_expired = True
		# self.check_perf("cooldown", start, False)
		return is_expired

if __name__ == '__main__':
	bot = Bot()
	P = PlayerKeyboard(bot)
	P.start()
	bot.main()