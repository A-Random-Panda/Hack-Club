from ursina import *
import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.in_game.player import _Player

#function for shooting
def shoot(player:"_Player", reload:Audio, shooting:Audio):
    play_multi = 1 / (player.reload_time / 5)
    if player.reload_time < abs(time.perf_counter()-player.cd):
        hit = raycast(origin = player.world_position + player.forward,distance=1000, direction = player.forward)
        player.cd = time.perf_counter()
        shooting.pitch = play_multi
        reload.pitch = play_multi
        Sequence(Func(shooting.play),
                Wait(0.9 / play_multi),
                Func(reload.play)).start()
        player.bullet_trail = Entity(model="cube",
                                    position= ((hit.world_point + player.world_position+player.forward)/2) + Vec3(0,1.7,0),
                                    scale = (0.2,0.2,distance(hit.world_point,player.world_position)),
                                    color = color.white,parent = scene,
                                    rotation = player.rotation,
                                    collider = "box"
                                    )
        destroy(player.bullet_trail,delay = 0.1)

#function for the reload timer
def reload_timer(player:"_Player",cooldown_text:Text):
    timer = "Shooting cooldown " + str(round(player.reload_time - time.perf_counter() +player.cd, 1))
    cooldown_text.text = timer if player.reload_time - (time.perf_counter()-player.cd) > 0 else "READY"



