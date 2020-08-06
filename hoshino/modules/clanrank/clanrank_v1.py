from hoshino import util
from hoshino.service import Service
import requests,json,time

sv = Service('clanrank', enable_on_default=True)

async def get_rank(bot, ctx, name):
	if name=="":
		config = util.load_config(__file__)
		clan_name = config["clanName"]
	else:
		clan_name = name
	url = "https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com/name/-1"
	name = json.dumps({ "clanName": clan_name })
	headers = {
		"Content-Type":"application/json",
		"Referer":"https://kengxxiao.github.io/Kyoka",
		"Origin":"https://kengxxiao.github.io"
	}
	r = requests.post(url,data=name,headers=headers)
	r_dec = json.loads(r.text)
	try:
		clanname = r_dec['data'][0]['clan_name']
		rank = r_dec['data'][0]['rank']
		damage = r_dec['data'][0]['damage']
		leader_name = r_dec['data'][0]['leader_name']
		leader_viewer_id = r_dec['data'][0]['leader_viewer_id']
		ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(r_dec['ts']))
		msg = f"\n>>>公会战排名查询\n公会名称：{clanname}\n公会会长：{leader_name}\n会长ID：{leader_viewer_id}\n目前排名：{rank}\n获得分数：{damage}\n数据时间：{ts}"
	except IndexError:
		msg = f"\n>>>公会战排名查询\n您查询的公会尚未参加公会战"
	await bot.send(ctx, msg, at_sender=True)

async def get_rank_seat(bot, ctx, seat):
	url = "https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com/rank/"+seat
	headers = {
		"Content-Type":"application/json",
		"Referer":"https://kengxxiao.github.io/Kyoka",
		"Origin":"https://kengxxiao.github.io"
	}
	r = requests.post(url,headers=headers)
	r_dec = json.loads(r.text)
	try:
		clan_name = r_dec['data'][0]['clan_name']
		rank = r_dec['data'][0]['rank']
		damage = r_dec['data'][0]['damage']
		leader_name = r_dec['data'][0]['leader_name']
		leader_viewer_id = r_dec['data'][0]['leader_viewer_id']
		ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(r_dec['ts']))
		msg = f"\n>>>公会战排名查询\n公会名称：{clan_name}\n公会会长：{leader_name}\n会长ID：{leader_viewer_id}\n目前排名：{rank}\n获得分数：{damage}\n数据时间：{ts}"
	except IndexError:
		msg = f"\n>>>公会战排名查询\n您查询的公会尚未参加公会战"
	await bot.send(ctx, msg, at_sender=True)


@sv.on_rex(r'^公会战排名(#.{1,20})?$',normalize=False)
async def rank_search(bot, ctx, match):
	try:
		name = match.group(1)[1:]
	except TypeError:
		name = ""
	await get_rank(bot, ctx, name)

@sv.on_rex(r'^公会战排名%(.{1,20})?$',normalize=False)
async def rank_search(bot, ctx, match):
	try:
		seat = match.group(1)
	except TypeError:
		msg = "语法错误，请使用\"公会战排名%查询排名\"进行查询。"
		await bot.send(ctx, msg, at_sender=True)
		return
	await get_rank_seat(bot, ctx, seat)