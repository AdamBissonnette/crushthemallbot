import autopy
import louie
import threading
import time
from datetime import datetime

def get_bitmap(file):
	return autopy.bitmap.Bitmap.open(file)

def refresh_screen(full=True):
	screen = None
	if full:
		screen = autopy.bitmap.capture_screen(((0,0), (390,730)))
	else:
		screen = autopy.bitmap.capture_screen(((0,0), (390,340)))
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
		get_bitmap('assets/chest_gold_step1.png'),
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
	functions = [
		get_bitmap('assets/decline.png'),
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
		get_bitmap('assets/ascend_step2_double.png'),
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
	]

	screen = refresh_screen()
	screen.save("screen.png")
	# return

	start_time = datetime.now()
	ascend_cooldown = (2400/15)*60
	dungeon_cooldown = 900
	weapon_cooldown = 0.7
	find_and_click_asset(screens)
	last_dungeon_run = None#datetime.now()
	last_weapon_run = None
	last_ascend = datetime.now()
	iteration = 0
	while True:
		# do_functions(functions)
		# return
		if check_cooldown(last_ascend, ascend_cooldown, log=True):
			screen = refresh_screen()
			screen.save("ascend{}.png".format(str(iteration)))
			do_ascend(ascend_steps)
			last_ascend = datetime.now()
			ascend_cooldown = (3600/17)*60
			time.sleep(1)
		# return

		speedad_run = do_speedad(speedad_steps)

		if check_cooldown(last_dungeon_run, dungeon_cooldown):
			do_dungeon(dungeon_steps)
			last_dungeon_run = datetime.now()
			time.sleep(1)
		# return

		if iteration % 30 == 0:
			time.sleep(0.5)
			switch_screens(screens)
		
		for i in range(1,4):
			if not speedad_run:
				do_chests(brown_chests, gold_chests)
				found_edge = find_asset(screen, edge)
				if found_edge:
					click_asset(found_edge, 2, 0, 20, sleep_after_click=0)
					do_chests(brown_chests, gold_chests)

			if check_cooldown(last_weapon_run, weapon_cooldown):
				weapon_run = do_weapons(weapons, edge)
				if weapon_run:
					last_weapon_run = datetime.now()
		
		if iteration % 10 == 0:
			do_collection(collections)
		elif iteration % 10 == 1:
			do_functions(functions)

		iteration = iteration + 1

def do_dungeon(dungeon_steps):
	find_and_click_asset(dungeon_steps[0])
	find_and_click_asset(dungeon_steps[1])
	find_and_click_asset(dungeon_steps[2])
	find_and_click_asset(dungeon_steps[3])
	# find_and_click_asset(dungeon_steps[4])
	time.sleep(10)
	autopy.key.tap(autopy.key.Code.ESCAPE)

def do_ascend(ascend_steps):
	if find_and_click_asset(ascend_steps[0], 3, tolerance=0.2, persistent=True):
		find_and_click_asset(ascend_steps[1])
		find_and_click_asset(ascend_steps[2])
		time.sleep(5)
		autopy.key.tap(autopy.key.Code.ESCAPE)
		time.sleep(1)
		autopy.key.tap(autopy.key.Code.ESCAPE)
		time.sleep(1)
		autopy.key.tap(autopy.key.Code.ESCAPE)
		time.sleep(1)

def do_speedad(speedad_steps):
	speedad_ready = find_and_click_asset(speedad_steps[0], tolerance=0.2)

	if speedad_ready:
		ad_launched = launch_ad(speedad_steps[1])
	
		if ad_launched:
			return True
	
	return False

def launch_ad(ad_asset, timeout=35):	
	screen = refresh_screen()

	ad_confirm = find_asset(screen, ad_asset, 0.2)

	if ad_confirm:
		click_asset(ad_confirm, 2)
		time.sleep(timeout)
		autopy.key.tap(autopy.key.Code.ESCAPE)
		time.sleep(2)
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
		click_asset(chest)
		time.sleep(0.2)

		if launch_ad(gold_chests[1]):
			time.sleep(5)
			screen = refresh_screen()
			confirm_reward = find_asset(screen, gold_chests[2])
			if confirm_reward:
				click_asset(confirm_reward)

def switch_screens(screens):
	find_and_click_asset(screens, 2)

def do_weapons(weapons, edge):
	screen = refresh_screen(False)
	weapon = find_asset(screen, weapons)
	found_edge = find_asset(screen, edge)

	if weapon is not None and found_edge is not None:
		click_asset(found_edge, 2, 0, 20, sleep_after_click=0.1)
		click_asset(weapon, 2, -2, -2, sleep_after_click=0)
		return True
	return False

def do_functions(functions):
	functions = find_and_click_asset(functions, 5, tolerance=0.1)

def do_collection(collections):
	find_and_click_asset(collections, 3, tolerance=0.2)

def find_and_click_asset(assets, click_x_times=2, xoffset=0, yoffset=0, tolerance=0, persistent=False):
	count = 1

	if persistent:
		count = 5

	for i in range(0, count):
		screen = refresh_screen()
		asset = find_asset(screen, assets, tolerance)
		if asset:
			click_asset(asset, click_x_times, xoffset, yoffset)
			time.sleep(0.1)
			return True
	return False

def find_asset(screen, assets, tolerance=0):
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

def click_asset(found_asset, count=2, xoffset=0, yoffset=0, sleep_after_click=0.2):
	autopy.mouse.move(found_asset[0]-xoffset, found_asset[1]-yoffset)
	for i in range(1,count):
		autopy.mouse.click()
		# autopy.mouse.toggle(down=True)
		time.sleep(sleep_after_click)
		# autopy.mouse.toggle(down=False)

main()