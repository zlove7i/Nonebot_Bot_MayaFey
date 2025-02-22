"""
@Author: Shine_Light
@Version: 1.0
@Date: 2022/8/5 19:55
"""
from nonebot import on_notice, on_command
from nonebot.adapters.onebot.v11 import GroupDecreaseNoticeEvent, GroupMessageEvent, Message
from nonebot.plugin import PluginMetadata
from utils import users
from utils.other import add_target
from utils.permission import special_per, get_special_per
from .tools import *


# 插件元数据定义
__plugin_meta__ = PluginMetadata(
    name="leave",
    description="离群提示",
    usage="/离群提示 {内容} (超级用户)\n"
          "/踢出提示 {内容} (超级用户)\n"
          "注:在内容中可以使用转义字符\n"
          "{leaved}表示退群的人,{kicked}表示被踢的人,{kicker}表示操作者" + add_target(60),
    extra={
        "generate_type": "group",
        "permission_common": "member",
        "unset": False,
        "total_unable": True,
        "author": "Shine_Light",
        "translate": "离群提示",
    }
)


# 离群事件
leave = on_notice(rule=checker_leave(), priority=4, block=False)
@leave.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    uid = str(event.get_user_id())
    gid = str(event.group_id)
    await init(gid)
    sub_type = event.sub_type
    operator_id = event.operator_id
    if sub_type == "leave":
        nickname = (await bot.get_stranger_info(user_id=int(uid), no_cache=True))["nickname"]
        msg = (await get_text(gid, "leave"))\
            .replace("{leaved}", nickname)\
            .replace("{leaved_id}", uid)
    elif sub_type == "kick":
        nickname_u = (await bot.get_stranger_info(user_id=int(uid), no_cache=True))["nickname"]
        nickname_o = (await bot.get_group_member_info(group_id=int(gid), user_id=int(operator_id), no_cache=True))["nickname"]
        msg = (await get_text(gid, "kick"))\
            .replace("{kicked}", nickname_u)\
            .replace("{kicker}", nickname_o)\
            .replace("{kicked_id}", uid)\
            .replace("{kicker_id}", str(operator_id))
    elif sub_type == "kick_me":
        return
    await leave.send(Message(msg))


leave_msg_update = on_command(cmd="离群提示", aliases={"退群提示"}, priority=7)
@leave_msg_update.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    gid = str(event.group_id)
    await init(gid)
    role = users.get_role(gid, str(event.user_id))
    if special_per(role, "leave_msg_update", gid):
        content = str(event.get_message()).split(" ", 1)[1]
        if content:
            await tools.update(content, gid, "leave")
            await leave_msg_update.send("修改成功")
        else:
            await leave_msg_update.send("内容不能为空")
    else:
        await leave_msg_update.finish(
            f"无权限,权限需在 {get_special_per(str(event.group_id), 'leave_msg_update')} 及以上")


kick_msg_update = on_command(cmd="踢出提示", priority=7)
@kick_msg_update.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    gid = str(event.group_id)
    await init(gid)
    role = users.get_role(gid, str(event.user_id))
    if special_per(role, "kicked_msg_update", gid):
        content = str(event.get_message()).split(" ", 1)[1]
        if content:
            await tools.update(content, gid, "kick")
            await kick_msg_update.send("修改成功")
        else:
            await kick_msg_update.send("内容不能为空")
    else:
        await kick_msg_update.finish(
            f"无权限,权限需在 {get_special_per(str(event.group_id), 'kicked_msg_update')} 及以上")
