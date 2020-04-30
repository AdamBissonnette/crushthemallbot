import autopy
import time
from datetime import datetime

def get_bitmap(file):
	return autopy.bitmap.Bitmap.open(file)

def refresh_screen():
	return autopy.bitmap.capture_screen()

def main():
	start_time = datetime.now()

	screens = [
		get_bitmap('assets/screen_heroes.png'),
		get_bitmap('assets/screen_village.png'),
		get_bitmap('assets/screen_battle.png')
	]
	chests = [
		get_bitmap('assets/chest_brown.png'),
		get_bitmap('assets/chest_brown2.png')
		# get_bitmap('assets/chest_gold.png'),
		# get_bitmap('assets/chest_gold2.png'),
		# get_bitmap('assets/chest_gold3.png')
	]
	weapons = [
		get_bitmap('assets/weapon_swords.png'),
		get_bitmap('assets/weapon_daggers.png'),
		get_bitmap('assets/weapon_blobs.png'),
		get_bitmap('assets/weapon_katana.png')
	]
	functions = [
		get_bitmap('assets/function_upgrade_heroes.png'),
		get_bitmap('assets/function_upgrade_villages.png'),
		get_bitmap('assets/function_collect.png')
	]
	edge = [get_bitmap('assets/edge.png')]

	ascend_steps = [
		get_bitmap('assets/ascend_step1.png'),
		get_bitmap('assets/ascend_step2.png'),
		get_bitmap('assets/ascend_step3.png'),
		get_bitmap('assets/ascend_step4.png'),
		get_bitmap('assets/ascend_step5.png'),
		get_bitmap('assets/ascend_step6.png')
	]


	dungeons = [get_bitmap('assets/function_dungeon_enter.png')]

	screen = refresh_screen()
	# print(find_every_asset(screen, dungeons))
	screen.save("screen.png")
	# return

	is_ascending = False
	ascend_step = 0

	# escape from add
	# time.sleep(2)
	# autopy.key.tap(autopy.key.Code.ESCAPE)
	# return

	while True:
		if not is_ascending:
			do_weapons(weapons, edge)
			do_functions(functions)
			do_chests(chests)
			do_weapons(weapons, edge)
			do_chests(chests)
			switch_screens(screens)
			time.sleep(0.5)

		# 	runtime = datetime.now() - start_time
		# 	if runtime.total_seconds() > 10:
		# 		is_ascending = True
		# else:
			

def do_chests(chests):
	screen = refresh_screen()
	chest = find_asset(screen, chests)
	if chest:
		click_asset(chest)
		time.sleep(0.1)

def switch_screens(screens):
	screen = refresh_screen()
	new_screen = find_asset(screen, screens)
	if new_screen:
		click_asset(new_screen)
		time.sleep(0.2)

def do_weapons(weapons, edge):
	screen = refresh_screen()
	weapon = find_asset(screen, weapons)
	found_edge = find_asset(screen, edge)
	if weapon is not None and found_edge is not None:
		click_asset(found_edge, 4, 0, 20)
		time.sleep(0.1)
		click_asset(weapon, 2, -2, -2)

def do_functions(functions):
	screen = refresh_screen()
	function = find_asset(screen, functions)
	if function:
		click_asset(function, 5)
		time.sleep(0.1)

def find_asset(screen, assets):
	for asset in assets:
		found_asset = screen.find_bitmap(asset)
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

def click_asset(found_asset, count=2, xoffset=0, yoffset=0):
	autopy.mouse.move(found_asset[0]-xoffset, found_asset[1]-yoffset)
	for i in range(1,count):
		autopy.mouse.click()

main()