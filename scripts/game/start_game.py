from ursina import *
from scripts.game.settings import *
from typing import TYPE_CHECKING
import time
if TYPE_CHECKING:
    from scripts.game.player import _Player
    from scripts.game.audio_controller import AudioController
    from scripts.game.ui import UIController


def destory_all_cameras(player: "_Player", ui: "UIController"):
        player.current_cam = 0
        for i in range(1,len(player.perspective_list)):
            destroy(player.perspective_list[i])
        for icons in player.cam_icon_list:
            destroy(icons)
        player.in_camera = False
        camera.parent = player.camera_pivot
        ui.camoverlay.disable()
        player.perspective_list.clear()
        player.perspective_list.append(player)

def reset_values(player:"_Player",ui:"UIController", enemy_id:int, your_id:int):
    if enemy_id > your_id:
        player.respawn_point = RESPAWN_POINTS[0]
        player.rotation_y = RESPAWN_ROTATION[0]
    else:
        player.respawn_point = RESPAWN_POINTS[1]
        player.rotation_y = RESPAWN_ROTATION[1]
    player.position = player.respawn_point
    player.cash = 1000
    ui.close_all_uis()
    player.points = 0
    player.max_cams = 6
    player.reload_time = 5
    ui.current_cash.text = f"{player.cash} cash"
    ui.faster_reload_button.text = f"-0.5 sec reload time \n reload time: {player.reload_time} sec \n cost: $100"
    ui.upgrade_cams_button.text = f"+1 Max cam \n current cams: {player.max_cams} \n cost: $100"
    ui.leaderboard_text.text = f"{player.points} {player.username} \n round wins: {player.round_wins}"
    ui.enemy_leaderboard_text.text = f""
    player.round_wins = 0
    ui.game_lose.enabled = False
    ui.game_win.enabled = False

    destory_all_cameras(player, ui)

def end_round(player:"_Player", ui:"UIController", points:int):
    ui.win_text.text = f'{player.username} WINS!!!'
    ui.lose_text.text =f'{player.username} LOSES!!!'
    ui.draw_text.text =f'{player.username} DRAWS!!!'
    player.rounds += 1
    if player.points > points:
        ui.win_text.enabled = True
        invoke(setattr, ui.win_text, "enabled", False, delay = 10)
        player.cash += WIN_BONUS * player.rounds
        player.round_wins += 1
        player.lose_streak = 0

    elif player.points < points:
        player.cash += LOSS_BONUS[player.lose_streak] * player.rounds
        ui.lose_text.enabled = True
        invoke(setattr, ui.lose_text, "enabled", False, delay = 10)

    else:
        ui.draw_text.enabled = True
        player.cash += DRAW_BONUS * player.rounds
        invoke(setattr, ui.draw_text, "enabled", False, delay = 10)
    ui.menu_overlay.enabled = True
    ui.current_cash.text = f"{player.cash} cash"
    invoke(setattr, ui.menu_overlay, "enabled", False, delay = 10)
    player.points = 0
    
def buy_phase(player:"_Player", ui:"UIController", state = True):
    player.in_buy_phase = state
    ui.buy_overlay.enabled = state
    ui.buy_text.enabled = state
    player.in_round = not state
    ui.shop_timer_text.enabled = state
    if state:
        player.shop_timer = time.perf_counter()

def start_round(player:"_Player", ui:"UIController", enemy_id:int, your_id:int):
    if enemy_id > your_id:
        player.respawn_point = RESPAWN_POINTS[0]
        player.rotation_y = RESPAWN_ROTATION[0]
    else:
        player.respawn_point = RESPAWN_POINTS[1]
        player.rotation_y = RESPAWN_ROTATION[1]
    
    player.in_round = True
    player.round_timer = time.perf_counter()
    buy_phase(player, ui, False)
    ui.round_timer_text.enabled = True
    player.position = player.respawn_point
    
def end_game(player:"_Player", ui:"UIController"):
    pass
