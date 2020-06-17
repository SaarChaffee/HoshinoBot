import random
from datetime import timedelta

from nonebot import on_command
from hoshino import util
from hoshino.res import R
from hoshino.service import Service, Privilege as Priv

# basic function for debug, not included in Service('chat')


@on_command('zai?', aliases=('在?', '在？', '在吗', '在么？', '在嘛', '在嘛？'))
async def say_hello(session):
    await session.send('あなたのために言っておくけど、私からは少なくとも2メートル以上離れることね...')

sv = Service('chat', manage_priv=Priv.SUPERUSER, visible=False)


@sv.on_command('沙雕机器人', aliases=('沙雕機器人',), only_to_me=False)
async def say_sorry(session):
    await session.send('ごめんなさい！')


@sv.on_command('老婆', aliases=('waifu', 'laopo'), only_to_me=True)
async def chat_waifu(session):
    await session.send('まったく、あなたという人は本当に頑固ね...', at_sender=True)


@sv.on_command('老公', only_to_me=True)
async def chat_laogong(session):
    await session.send('死ぬ！', at_sender=True)


@sv.on_command('mua', only_to_me=True)
async def chat_mua(session):
    await session.send('バカ!', at_sender=True)


@sv.on_command('我有个朋友说他好了', aliases=('我朋友说他好了', ), only_to_me=False)
async def ddhaole(session):
    await session.send('その友達はあなたですか？')


@sv.on_command('我好了', only_to_me=False)
async def nihaole(session):
    await session.send('だめだ、やめろ！')


# # ============================================ #


# @sv.on_keyword(('确实', '有一说一', 'u1s1', 'yysy'))
# async def chat_queshi(bot, ctx):
#     if random.random() < 0.05:
#         await bot.send(ctx, R.img('确实.jpg').cqcode)


# @sv.on_keyword(('会战', '刀'))
# async def chat_clanba(bot, ctx):
#     if random.random() < 0.03:
#         await bot.send(ctx, R.img('我的天啊你看看都几度了.jpg').cqcode)


# @sv.on_keyword(('内鬼'))
# async def chat_neigui(bot, ctx):
#     if random.random() < 0.10:
#         await bot.send(ctx, R.img('内鬼.png').cqcode)
