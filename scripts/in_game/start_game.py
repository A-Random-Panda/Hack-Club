from ursina import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.in_game.player import _Player
    from scripts.in_game.audio_controller import AudioController
    from scripts.in_game.ui import UIController


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

def start_game(player:"_Player",ui:"UIController"):
    player.position = player.respawn_point
    player.cash = 1000
    ui.close_all_uis()
    player.points = 0
    player.max_cams = 5
    player.reload_time = 5
    ui.current_cash.text = f"{player.cash} cash"
    ui.faster_reload_button.text = f"-0.5 sec reload time \n reload time: {player.reload_time} sec \n cost: $500"
    ui.upgrade_cams_button.text = f"+1 Max cam \n current cams: {player.max_cams} \n cost: $500"
    ui.leaderboard_text.text = f"{player.points} {player.username}"

    destory_all_cameras(player, ui)

def end_round(player:"_Player", ui:"UIController"):
    ui.win_text.text = f'{player.username} WINS!!!'
    ui.lose_text.text =f'{player.username} LOSES!!!'
    ui.draw_text.text =f'{player.username} DRAWS!!!'
    if player.points > 100:
        ui.win_text.enabled = True
        invoke(setattr, ui.win_text, "enabled", False, delay = 10)
    elif player.points < 100:
        ui.lose_text.enabled = True
        invoke(setattr, ui.lose_text, "enabled", False, delay = 10)
    else:
        ui.draw_text.enabled = True
        invoke(setattr, ui.draw_text, "enabled", False, delay = 10)
    start_game(player, ui)
    ui.menu_overlay.enabled = True
    invoke(setattr, ui.menu_overlay, "enabled", False, delay = 10)