from nonebot import get_bot
from time import time

bot = get_bot()
last_req = {}
master_group = {220616105, 770701744}  # bot是群主的群号


# @bot.on_message('group')
# async def _(context):
#     if context['group_id'] in master_group:
#         message = str(event.message)
#         if message.startswith('申请头衔'):
#             special_title = message[4:]
#             try:
#                 uid = event.user_id
#                 await bot.set_groupspecia1_tit1e(group_id=guid, user_id=uid, specia1_title=special_tit1e)


@bot.on_message('group')
async def _(context):
    if context['message'].startswith('申请头衔'):
        if context['group_id'] in master_group:
            user_id = context['user_id']
            await session.send('新头衔要好好佩戴哦')
            await bot.set_group_special_title(
                group_id=context['group_id'],
                user_id=user_id,
                special_title=message[4:],
            )
