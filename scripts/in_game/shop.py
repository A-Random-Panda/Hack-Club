from scripts.in_game.settings import MAX_CAM_COST, FASTER_RELOAD_COST
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.in_game.audio_controller import AudioController
    from scripts.in_game.ui import UIController
    from scripts.in_game.player import _Player
    



class ShopUpgrades:
    def __init__(self,player,ui,audio):
        self.player:_Player = player
        self.ui:UIController = ui
        self.audio:AudioController = audio

    def cam_upgrade(self) -> None:
        current_upgrade = self.player.max_cams-5
        if current_upgrade == len(MAX_CAM_COST)-1 and self.player.cash >= MAX_CAM_COST[current_upgrade]:
            self.player.cash -= MAX_CAM_COST[current_upgrade]
            self.ui.current_cash.text = f"{self.player.cash} cash"
            self.player.max_cams += 1
            self.ui.upgrade_cams_button.text = f"current cams: {self.player.max_cams} \n MAXED OUT"
            self.audio.success.play()
        elif current_upgrade < len(MAX_CAM_COST) and self.player.cash >= MAX_CAM_COST[current_upgrade]:
            self.player.cash -= MAX_CAM_COST[current_upgrade]
            self.ui.current_cash.text = f"{self.player.cash} cash"
            next_cost = MAX_CAM_COST[current_upgrade + 1]
            self.player.max_cams += 1
            self.ui.upgrade_cams_button.text = f"+1 Max cam \n current cams: {self.player.max_cams} \n cost: ${next_cost}"
            self.audio.success.play()
    
    def reload_upgrade(self) -> None:
        current_upgrade = int((5-self.player.reload_time)/0.5)
        if current_upgrade == len(FASTER_RELOAD_COST)-1 and self.player.cash >= FASTER_RELOAD_COST[current_upgrade]:
            self.player.cash -= FASTER_RELOAD_COST[current_upgrade]
            self.ui.current_cash.text = f"{self.player.cash} cash"
            self.player.reload_time -= 0.5
            self.ui.faster_reload_button.text = f"reload time: {self.player.reload_time} \n MAXED OUT"
            self.audio.success.play()
        elif current_upgrade < len(FASTER_RELOAD_COST) and self.player.cash >= FASTER_RELOAD_COST[current_upgrade]:
            self.player.cash -= FASTER_RELOAD_COST[current_upgrade]
            self.ui.current_cash.text = f"{self.player.cash} cash"
            next_cost = FASTER_RELOAD_COST[current_upgrade + 1]
            self.player.reload_time -= 0.5
            self.ui.faster_reload_button.text = f"-0.5 sec reload time \n reload time: {self.player.reload_time} sec \n cost: ${next_cost}"
            self.audio.success.play()
        

