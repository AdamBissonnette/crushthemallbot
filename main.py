import autopy
# import louie
# import threading
import time
# import pynput
from datetime import datetime

def get_bitmap(file):
	return autopy.bitmap.Bitmap.open(file)

def refresh_screen(full=True):
	screen = None
	if full:
		screen = autopy.bitmap.capture_screen(((0,0), (390,730)))
	else:
		screen = autopy.bitmap.capture_screen(((0,0), (390,380)))
	return screen

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

def main():
	screens = [
		get_bitmap('assets/screen_heroes.png'),
		get_bitmap('assets/screen_village.png'),
	]
	brown_chests = [
		get_bitmap('assets/chest_brown.png'),
		get_bitmap('assets/chest_brown2.png'),
		get_bitmap('assets/chest_brown3.png'),
	]
	gold_chests = [
		[
			get_bitmap('assets/chest_gold_step1.png'),
			get_bitmap('assets/chest_gold2.png'),
			get_bitmap('assets/chest_gold3.png'),
		],
		get_bitmap('assets/chest_gold_step2.png'),
		get_bitmap('assets/chest_gold_step3.png'),
	]
	weapons = [
		get_bitmap('assets/weapon_swords.png'),
		get_bitmap('assets/weapon_daggers.png'),
		get_bitmap('assets/weapon_blobs.png'),
		get_bitmap('assets/weapon_fireball.png'),
		get_bitmap('assets/weapon_katana.png'),
	]

	decline = get_bitmap('assets/decline.png')
	cta_app = get_bitmap('assets/crush_them_all_app.png')

	functions = [
		cta_app,
		decline,
		get_bitmap('assets/okay.png'),
		get_bitmap('assets/X.png'),
		get_bitmap('assets/chest_gold_step3.png'),
		get_bitmap('assets/function_upgrade_heroes.png'),
		get_bitmap('assets/function_upgrade_villages.png'),
	]
	collections = [
		get_bitmap('assets/function_collect.png'),
	]
	edge = [get_bitmap('assets/edge.png')]

	speedad_steps = [
		get_bitmap('assets/speedad_step1.png'),
		get_bitmap('assets/accept.png')
	]

	ascend_steps = [
		get_bitmap('assets/ascend_step1.png'),
		[get_bitmap('assets/ascend_step2.png')],
		get_bitmap('assets/ascend_accept.png'),
		get_bitmap('assets/ascend_step4.png'),
		get_bitmap('assets/ascend_step5.png')
	]

	dungeon_steps = [
		get_bitmap('assets/screen_battle.png'),
		get_bitmap('assets/dungeon_step1.png'),
		get_bitmap('assets/dungeon_step2.png'),
		get_bitmap('assets/dungeon_step3.png'),
		get_bitmap('assets/decline.png'),
		get_bitmap('assets/dungeon_edge.png'),
		get_bitmap('assets/dungeon_okay.png'),
	]

	expedition_steps = [
		get_bitmap('assets/exped_step0_reward_ready.png'),
		get_bitmap('assets/screen_battle.png'),
		get_bitmap('assets/exped_step1.png'),
	]

	exped_start = [
		[get_bitmap('assets/exped_step2_run.png'),
		get_bitmap('assets/exped_step2_run2.png')],
		get_bitmap('assets/exped_step3_autofill.png'),
		get_bitmap('assets/exped_step4_start.png'),
	]

	exped_collect = [
		[get_bitmap('assets/exped_step5_collect.png'),
		get_bitmap('assets/exped_step5_collect2.png'),
		get_bitmap('assets/exped_step5_collect3.png')
		],
		get_bitmap('assets/exped_step6_confirm.png'),
	]

	screen = refresh_screen()
	screen.save("screen.png")
	# return

	ascend_cooldown = (2700/17)*60
	dungeon_cooldown = 1200
	exped_cooldown = 600
	weapon_cooldown = 1
	find_and_click_asset(screens)
	last_dungeon_run = None #datetime.now()
	last_exped_run = datetime.now()
	last_weapon_run = None
	last_ascend = datetime.now()
	iteration = 0
	stopping = False
	while not stopping:
		# last_dungeon_run = do_dungeon(dungeon_cooldown,
		# 								last_dungeon_run,
		# 								dungeon_steps,
		# 								decline,
		# 								weapons,
		# 								edge)
		# return
		# last_exped_run = do_expedition(exped_cooldown, last_exped_run, expedition_steps, exped_start, exped_collect)
		# do_functions(functions)
		# check_if_ad_is_done(5)
		# do_weapons(weapons, edge)
		# return
		if check_cooldown(last_ascend, ascend_cooldown, log=True):
			# screen = refresh_screen()
			# screen.save("ascend{}.png".format(str(iteration)))
			ascended = do_ascend(ascend_steps)
			if ascended:
				last_ascend = datetime.now()
				ascend_cooldown = (3500/17)*60
				time.sleep(1)
		# return

		speedad_run = do_speedad(speedad_steps)
		last_dungeon_run = do_dungeon(dungeon_cooldown,
										last_dungeon_run,
										dungeon_steps,
										decline,
										weapons,
										edge)
		last_exped_run = do_expedition(exped_cooldown,
										last_exped_run,
										expedition_steps,
										exped_start,
										exped_collect)
		# return

		if iteration % 15 == 0:
			# time.sleep(0.5)
			switch_screens(screens)
		
		for _ in range(1,4):
			if not speedad_run:
				do_chests(brown_chests, gold_chests)
				found_edge = find_asset(screen, edge)
				if found_edge:
					click_asset(found_edge, 2, 0, -35, sleep_after_click=0)
					do_chests(brown_chests, gold_chests)

			if check_cooldown(last_weapon_run, weapon_cooldown):
				weapon_run = do_weapons(weapons, edge)
				if weapon_run:
					last_weapon_run = datetime.now()
		
		if iteration % 3 == 0:
			do_collection(collections)
		elif iteration % 4 == 1:
			do_functions(functions)

		iteration = iteration + 1

def do_expedition(exped_cooldown, last_exped_run, expedition_steps, exped_start, exped_collect):
	reward_ready = find_asset(expedition_steps[0], tolerance=0.2)

	if reward_ready or check_cooldown(last_exped_run, exped_cooldown):
		in_exped = do_steps([expedition_steps[1], expedition_steps[2]])
		collected = do_steps(exped_collect, loop=True, tolerance=0.3)
		started = do_steps(exped_start, loop=True, tolerance=0.3)

		# print(in_exped, collected, started)

		if in_exped:
			escape_back(2)

		return datetime.now()
	return last_exped_run

def do_steps(steps, delay=1, loop=False, tolerance=0.2):
	completed_once = False
	clicked_step = True
	while clicked_step:
		for step in steps:
			step_done = find_and_click_asset(step, tolerance=tolerance)
			if not step_done:
				clicked_step = False
				continue
			time.sleep(delay)
		if step_done:
			completed_once = True
	return completed_once

def escape_back(times=1):
	for _ in range(0, times):
		autopy.key.tap(autopy.key.Code.ESCAPE)
		time.sleep(1)
		on_exit = is_on_exit()
		# print(on_exit)
		if on_exit:
			click_asset(on_exit)
			time.sleep(0.3)
			return

def is_on_exit():
	decline = get_bitmap('assets/decline.png')
	return find_asset(assets=decline, tolerance=0.2)

def scroll_up_from_asset(assets, distance):
	#toggle click on asset
	#slow move up
	#release click
	return

def is_out_of_app():
	app_screen = get_bitmap('assets/crush_them_all_app.png')

	if find_asset(assets=app_screen, tolerance=0.2):
		return True
	return False

def is_in_main_area():
	main_area_markers = [
		get_bitmap('assets/screen_heroes.png'),
		get_bitmap('assets/screen_village.png'),
	]

	if find_asset(assets=main_area_markers, tolerance=0.2):
		return True
	return False

def do_dungeon(dungeon_cooldown, last_dungeon_run, dungeon_steps, decline, weapons, edge):
	if check_cooldown(last_dungeon_run, dungeon_cooldown):
		new_dungeon_runtime = datetime.now()

	do_steps([dungeon_steps[0], dungeon_steps[1], dungeon_steps[2], dungeon_steps[3]], delay=0.3)

	decline_found = find_and_click_asset(decline, tolerance=0.2)

	if is_in_main_area():
		return last_dungeon_run

	if not decline_found:
		time.sleep(0.5)
		victory = False
		while not victory:
			time.sleep(4)
			victory = do_dungeon_boss(weapons, dungeon_steps[5], dungeon_steps[6])

	return new_dungeon_runtime

		# do_dungeon_boss(dunweapons, edge)
		# autopy.key.tap(autopy.key.Code.ESCAPE)

	# find_and_click_asset(dungeon_steps[4])
	# reward_accepted = False
	# while not reward_accepted:
	# 	time.sleep(3)
	# 	reward_accepted = find_and_click_asset(dungeon_steps[4])


def do_dungeon_boss(weapons, edge, confirmation):
	do_weapons(weapons, edge, 0.3)
	time.sleep(1)

	get_rewards = find_and_click_asset(confirmation, tolerance=0.2)
	if not get_rewards:
		return False
	return True

def do_ascend(ascend_steps):
	if find_and_click_asset(ascend_steps[0], 3, tolerance=0.2, persistent=True):
		if find_and_click_asset(ascend_steps[1]):
			find_and_click_asset(ascend_steps[2])
			time.sleep(5)
			escape_back()
			time.sleep(1)
			escape_back()
			time.sleep(1)
			escape_back()
			time.sleep(1)
			return True
		else:
			return False
	else:
		return False

def do_speedad(speedad_steps):
	speedad_ready = find_and_click_asset(speedad_steps[0], tolerance=0.2)

	if speedad_ready:
		ad_launched = launch_ad(speedad_steps[1])
	
		if ad_launched:
			return True
	
	return False

def launch_ad(ad_asset, timeout=7):
	screen = refresh_screen()

	ad_confirm = find_asset(screen, ad_asset, 0.2)

	if ad_confirm:
		click_asset(ad_confirm, 2)
		time.sleep(timeout)

		#check to see if the ad launched properly (look for ascend?)
		if is_in_main_area():
			return False
		
		if is_out_of_app():
			return False

		ad_complete = False
		adtimeout = 60
		adstart = datetime.now()
		while not ad_complete :
			if check_cooldown(adstart, adtimeout):
				print("restarting app")
				restart_app()
				return False
			ad_complete = check_if_ad_is_done(7)

			if ad_complete:
				return True
	else:
		return False

def restart_app():
	exit_app()
	time.sleep(10)
	open_app()
	time.sleep(10)

def open_app():
	app_opened = False
	while not app_opened:
		app_opened = find_and_click_asset(get_bitmap("assets/crush_them_all_app.png"))
	print ("app opened")

def exit_app():
	autopy.key.tap(autopy.key.Code.PAGE_UP)
	time.sleep(5) #takes a while for the X to appear
	find_and_click_asset(get_bitmap("assets/gamequit.png"))
	

def check_if_ad_is_done(timeout):
	escape_back()

	time.sleep(1)

	screen = refresh_screen()
	resume_button = [
					get_bitmap("assets/ad_resume.png"), 
					get_bitmap("assets/ad_resume2.png"),
					get_bitmap("assets/ad_resume3.png"),
					]
	resume_found = find_asset(screen, resume_button, tolerance=0.2)
	if resume_found:
		click_asset(resume_found, 1)
		time.sleep(timeout)
		return False
	else:
		screen = refresh_screen()
		ad_complete_needle = get_bitmap('assets/screen_battle.png')
		ad_complete = find_asset(screen, ad_complete_needle, tolerance=0.2)
		if ad_complete:
			return True
		else:
			return False

def do_chests(brown_chests, gold_chests):
	screen = refresh_screen(False)
	chest = find_asset(screen, brown_chests, 0.3)

	if chest:
		click_asset(chest)

	#gold_chests	
	screen = refresh_screen(False)
	chest = find_asset(screen, gold_chests[0], 0.3)
	if chest:
		click_asset(chest, 2)
		time.sleep(0.2)

		if launch_ad(gold_chests[1]):
			time.sleep(1)
			screen = refresh_screen()
			confirm_reward = find_asset(screen, gold_chests[2])
			if confirm_reward:
				click_asset(confirm_reward)

def switch_screens(screens):
	find_and_click_asset(screens)

def do_weapons(weapons, edge, tolerance=0):
	screen = refresh_screen(False)
	weapon = find_asset(screen, weapons, tolerance=tolerance)
	found_edge = find_asset(screen, edge)

	if weapon is not None and found_edge is not None:
		click_asset(found_edge, 1, 0, -35, sleep_after_click=0.1)
		click_asset(weapon, 1, 5, 5, sleep_after_click=0)
		return True
	return False

def do_functions(functions):
	functions = find_and_click_asset(functions, 5, tolerance=0.1)

def do_collection(collections):
	find_and_click_asset(collections, 2, tolerance=0.2)

def find_and_click_asset(assets, click_x_times=1, xoffset=0, yoffset=0, tolerance=0, persistent=False, sleep_after_click=0.2):
	count = 1

	if persistent:
		count = 5

	for _ in range(0, count):
		screen = refresh_screen()
		asset = find_asset(screen, assets, tolerance)
		if asset:
			click_asset(asset, click_x_times, xoffset, yoffset, sleep_after_click)
			time.sleep(0.1)
			return True
	return False

def find_asset(screen=None, assets=None, tolerance=0):
	if assets is None:
		return None

	if screen is None:
		screen = refresh_screen()

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

def find_every_asset(screen, assets):
	found_assets = []

	for asset in assets:
		found_asset = screen.find_every_bitmap(asset)
		if found_asset:
			found_assets.append(found_asset)

	return found_assets

def click_asset(found_asset, count=1, xoffset=0, yoffset=0, sleep_after_click=0.2):
	autopy.mouse.move(found_asset[0]+xoffset, found_asset[1]+yoffset)
	for _ in range(0,count):
		autopy.mouse.click()
		time.sleep(sleep_after_click)

main()