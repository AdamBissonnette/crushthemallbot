import autopy
import time
from datetime import datetime

def get_bitmap(file):
	return autopy.bitmap.Bitmap.open(file)

def refresh_screen():
	return autopy.bitmap.capture_screen(((0,0), (550,1030)))

def main():
	start_time = datetime.now()

	screens = [
		get_bitmap('assets/screen_heroes.png'),
		get_bitmap('assets/screen_village.png'),
	]
	brown_chests = [
		get_bitmap('assets/chest_brown2.png')
	]
	gold_chests = [
		get_bitmap('assets/chest_gold2.png'),
	]
	weapons = [
		get_bitmap('assets/weapon_swords.png'),
		get_bitmap('assets/weapon_daggers.png'),
		get_bitmap('assets/weapon_blobs.png'),
		get_bitmap('assets/weapon_katana.png')
	]
	functions = [
		get_bitmap('assets/function_collect.png'),
		get_bitmap('assets/function_upgrade_heroes.png'),
		get_bitmap('assets/function_upgrade_villages.png'),
	]
	edge = [get_bitmap('assets/edge.png')]

	speedad_steps = [
		get_bitmap('assets/speedad_step1.png'),
		get_bitmap('assets/speedad_step2.png')
	]

	ascend_steps = [
		get_bitmap('assets/ascend_step1.png'),
		get_bitmap('assets/ascend_step2.png'),
		get_bitmap('assets/ascend_step3.png'),
		get_bitmap('assets/ascend_step4.png'),
		get_bitmap('assets/ascend_step5.png'),
		get_bitmap('assets/ascend_step6.png')
	]

	battle = [
		get_bitmap('assets/screen_battle.png'),
		get_bitmap('assets/function_dungeon_enter.png')
	]

	screen = refresh_screen()
	# print(find_every_asset(screen, dungeons))
	# screen.save("screen.png")
	# return

	is_ascending = False
	ascend_step = 0

	# escape from add
	# time.sleep(2)
	# autopy.key.tap(autopy.key.Code.ESCAPE)
	# return

	while True:
		if not is_ascending:
			find_and_click_asset(screens)
			switch_screens(screens)
			time.sleep(1)

			do_functions(functions)
			do_speedad(speedad_steps)
			do_weapons(weapons, edge)
			do_chests(brown_chests, gold_chests)
			do_weapons(weapons, edge)
			do_chests(brown_chests, gold_chests)
			do_weapons(weapons, edge)
			do_chests(brown_chests, gold_chests)
			do_weapons(weapons, edge)
			do_chests(brown_chests, gold_chests)

		# 	runtime = datetime.now() - start_time
		# 	if runtime.total_seconds() > (60*120) :
		# 		is_ascending = True
		# else:
		# 	print ("ascending!!!")
		# 	return

def do_speedad(speedad_steps):
	screen = refresh_screen()
	speedad_ready = find_asset(screen, speedad_steps[0], 0.2)

	if speedad_ready:
		click_asset(speedad_ready, 2)
		time.sleep(0.5)
		ad_launched = launch_ad(speedad_steps[1])
		if not ad_launched:
			return

def launch_ad(ad_asset, timeout=35):	
	screen = refresh_screen()
	ad_confirm = find_asset(screen, ad_asset)

	if ad_confirm:
		click_asset(ad_confirm, 2)
		time.sleep(timeout)
		autopy.key.tap(autopy.key.Code.ESCAPE)
		return True
	else:
		return False

def do_chests(brown_chests, gold_chests):
	screen = refresh_screen()
	chest = find_asset(screen, brown_chests, 0.3)

	if chest:
		click_asset(chest)
	
	# screen = refresh_screen()
	# chest = find_asset(screen, gold_chests, 0.4)
	# if chest:
	# 	click_asset(chest)

def switch_screens(screens):
	find_and_click_asset(screens, 2)

def do_weapons(weapons, edge):
	screen = refresh_screen()
	weapon = find_asset(screen, weapons)
	found_edge = find_asset(screen, edge)

	if weapon is not None and found_edge is not None:
		click_asset(found_edge, 2, 0, 20)
		time.sleep(0.1)
		click_asset(found_edge, 2, 0, 20)
		time.sleep(0.1)
		click_asset(weapon, 2, -2, -2)
		time.sleep(0.1)

def do_functions(functions):
	find_and_click_asset(functions, 2, tolerance=0.4)

def find_and_click_asset(assets, click_x_times=1, xoffset=0, yoffset=0, tolerance=0):
	screen = refresh_screen()
	asset = find_asset(screen, assets)
	if asset:
		click_asset(asset, click_x_times, xoffset, yoffset)
		time.sleep(0.1)

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

def click_asset(found_asset, count=2, xoffset=0, yoffset=0):
	autopy.mouse.move(found_asset[0]-xoffset, found_asset[1]-yoffset)
	for i in range(1,count):
		autopy.mouse.click()
		# autopy.mouse.toggle(down=True)
		time.sleep(0.2)
		# autopy.mouse.toggle(down=False)

main()