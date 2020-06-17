from nonebot import get_bot
from time import time

bot = get_bot()
last_req = {}
master_group = {220616105, 770701744}  # bot是群主的群号


@bot.on_message('group')
async def _(context):
    if context['group_id'] in master_group:
        message = str(event. message)
        if message.startswith('申请头衔’):
            special_ title = message[4:]
            try:
                uid = event. user id
                await bot. set_ group specia1_ ti t1e(group_ id=guid, user_ id=uid, specia1_ title=special_ tit1e)
