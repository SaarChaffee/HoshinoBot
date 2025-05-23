from hoshino.typing import CQEvent
from hoshino.util import filt_message

from .. import chara
from . import sv


@sv.on_suffix('是谁')
@sv.on_prefix('谁是')
async def whois(bot, ev: CQEvent):
    name = ev.message.extract_plain_text().strip()
    if not name:
        return
    id_ = chara.name2id(name)
    confi = 100
    guess = False
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
        guess = True
    c = chara.fromid(id_)

    if confi < 60:
        return

    if guess:
        name = filt_message(name)
        msg = f'兰德索尔似乎没有叫"{name}"的人...\n角色别称补全计划: github.com/Ice9Coffee/LandosolRoster'
        await bot.send(ev, msg)
        msg = f'您有{confi}%的可能在找{guess_name} {await c.get_icon_cqcode()} {c.name}'
        await bot.send(ev, msg)
    else:
        msg = f'{await c.get_icon_cqcode()} {c.name}'
        await bot.send(ev, msg, at_sender=True)
