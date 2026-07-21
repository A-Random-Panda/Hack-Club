from ursina import Audio
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.game.player import _Player

PLAYER_VOLUME = 1
SHOOTING_VOLUME = 0.5
RELOAD_VOLUME = 0.83

class AudioController():
    def __init__(self, player: "_Player"):
        self.shooting = Audio("sniper_shot",autoplay=False, volume= SHOOTING_VOLUME, spatial = True, parent = player)
        self.reload = Audio("reload", autoplay = False, volume = RELOAD_VOLUME, spatial = True)
        self.death = Audio("death",autoplay = False, volume = PLAYER_VOLUME, spatial = True, parent = player)
        self.success = Audio("success",autoplay = False, volume = PLAYER_VOLUME, spatial = True)
        self.footsteps = Audio("footsteps", autoplay = False, volume = PLAYER_VOLUME, spatial = True,parent = player)
        self.jump = Audio("jump", autoplay = False, volume = PLAYER_VOLUME, spatial = True, parent = player)
        self.audiolist = [self.shooting, self.reload,self.death, self.success, self.footsteps, self.jump]

    def stop_audio(self) -> None:
        for audio in self.audiolist:
            audio.stop()
        
    def set_gun_volume(self, value:float) -> None:
        self.shooting.volume = value/100
        self.reload.volume = value/60

    def set_player_volume(self, value:float) -> None:
        self.death.volume = value/50
        self.success.volume = value/50
        self.footsteps.volume = value/50
        self.jump.volume = value/50
