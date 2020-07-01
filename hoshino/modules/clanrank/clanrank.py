from hoshino import util
from hoshino.service import Service
import requests,json

sv = Service('clanrank', enable_on_default=True)

async def get_rank(bot, ctx, name):
	if name=="":
		config = util.load_config(__file__)
		clan_name = config["clanName"]
	else:
		clan_name = name
	url = "https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com/name/-1"
	name = json.dumps({ "clanName": clan_name })
	headers = {"Content-Type":"application/json"}
	r = requests.post(url,data=name,headers=headers)
	r_dec = json.loads(r.text)
	try:
		clanname = r_dec['data'][0]['clan_name']
		rank = r_dec['data'][0]['rank']
		damage = r_dec['data'][0]['damage']
		msg = f"\n>>>公会战排名查询\n公会名称：{clan_name}\n目前排名：{rank}\n造成伤害：{damage}"
	except IndexError:
		msg = f"\n>>>公会战排名查询\n您的公会尚未参加公会战"
	await bot.send(ctx, msg, at_sender=True)

@sv.on_rex(r'^公会战排名(#.{1,20})?$',normalize=False)
async def rank_search(bot, ctx, match):
	try:
		name = match.group(1)[1:]
	except TypeError:
		name = ""
	await get_rank(bot, ctx, name)