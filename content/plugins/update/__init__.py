"""
@Author: Shine_Light
@Version: 1.0
@Date: 2022/4/21 12:51
"""
from nonebot import on_command, require
from nonebot.exception import FinishedException
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment, Message
from . import tools


update = on_command("更新", aliases={"update"}, priority=2, block=True)
@update.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    try:
        if await tools.check_update():
            await update.send("检测到新版本,正在自动更新,更新期间机器人无法使用,请勿关闭程序")
            await tools.update(str(event.group_id))
            await update.send("正在重启...")
            await tools.reboot()
        else:
            await update.finish("已经是最新版本,无需更新")
    except FinishedException:
        pass
    except Exception as e:
        await update.send(f"更新出错: {str(e)}")


check_update = on_command("检查更新", aliases={"check_update"}, priority=8)
@check_update.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if await tools.check_update():
        await check_update.finish("检测到有新版本,请及时更新")
    else:
        await check_update.finish("已经是最新版本")


update_log = on_command("更新日志", aliases={"update_log", "更新记录"})
@update_log.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    img = await tools.get_update_log()
    await update_log.send(Message([MessageSegment.image(img),
                                   MessageSegment.text("完整日志地址:http://cdn.shinelight.xyz/nonebot/log.md")]))


timezone = "Asia/Shanghai"
scheduler = require("nonebot_plugin_apscheduler").scheduler
@scheduler.scheduled_job("cron", hour="8", minute="00", timezone=timezone)
async def run():
    if await tools.check_update():
        await check_update.finish("检测到有新版本,请及时更新")
