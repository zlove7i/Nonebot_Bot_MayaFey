"""
@Author: Shine_Light
@Version: 1.0
@Date: 2022/3/27 19:55
"""
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageEvent
from nonebot.exception import IgnoredException, ActionFailed
from nonebot.message import event_preprocessor
from nonebot.plugin import PluginMetadata
from utils.admin_tools import banSb, image_moderation_async
from utils.other import add_target
from utils import users
from .config import Config
from .data import Reqeust
from utils.permission import permission_

config = Config()

# 插件元数据定义
__plugin_meta__ = PluginMetadata(
    name="ban_pic",
    description="自动撤回违规图片",
    usage="被动,无命令" + add_target(60),
    extra={
        "generate_type": "group",
        "permission_common": "baned",
        "unset": False,
        "total_unable": True,
        "author": "Shine_Light",
        "translate": "违禁图检测",
    }
)


@event_preprocessor
async def check_pic(bot: Bot, event: GroupMessageEvent):
    msg = event.get_plaintext()
    if "初始化" in msg:
        return
    if "启用" in msg or "停用" in msg:
        return
    uid = event.get_user_id()
    gid = event.group_id
    eid = event.message_id
    if isinstance(event, MessageEvent):
        # 超级用户及以上不受影响
        if permission_(users.get_role(str(gid), str(uid)), "superuser"):
            return
        for msg in event.message:
            if msg.type == "image":
                url: str = msg.data["url"]
                if config.access_secret_baidu and config.access_key_baidu:
                    result = Reqeust(imgUrl=url).request()
                    if result.is_error():
                        logger.error("违禁图检测百度接口出错:" + result.error)
                    if result.is_illegal():
                        try:
                            await bot.delete_msg(message_id=eid)
                            logger.info('检测到违规图片,撤回')
                        except ActionFailed:
                            logger.info('检测到违规图片,但权限不足,撤回失败')
                        try:
                            await banSb(gid, ban_list=[uid], time=300)
                        except ActionFailed:
                            logger.info('检测到违规图片,但权限不足,禁言失败')
                        else:
                            await bot.send(event=event, message=f"发送了违规图片,类型{result.illegal_type},现对你进行处罚,有异议请联系管理员",
                                           at_sender=True)
                            logger.info(f"检测到违规图片,禁言操作成功,用户: {uid[0]}")
                        raise IgnoredException("违规图片")
                else:
                    image_ = url
                    # result = await pic_ban_cof(url=image_)
                    result = (await image_moderation_async(image_))
                    label = result["message"]
                    if label == "Porn":
                        label = "色情"
                    elif label == "Sexy":
                        label = "性感"
                    elif label == "Illegal":
                        label = "违法"
                    elif label == "Ad":
                        label = "广告"
                    elif label == "Terror":
                        label = "暴恐"
                    elif label == "Polity":
                        label = "政治"
                    elif label == "Abuse":
                        label = "谩骂"
                    # if label == "Illegal" or label == "Ad" or label == "Terror" or label == "Polity" or label == "Abuse":
                    #     result["status"] = True

                    if not result["status"]:
                        try:
                            await bot.delete_msg(message_id=eid)
                            logger.info('检测到违规图片, 撤回')
                        except ActionFailed:
                            logger.info('检测到违规图片, 但权限不足, 撤回失败')
                        try:
                            await banSb(gid, ban_list=[uid], time=300)
                        except ActionFailed:
                            logger.info('检测到违规图片, 但权限不足, 禁言失败')
                        else:
                            await bot.send(event=event, message=f"发送了违规图片,类型{label},现对你进行处罚,有异议请联系管理员", at_sender=True)
                            logger.info(f"检测到违规图片, 禁言操作成功, 用户: {uid[0]}")
                        logger.info('检测到违规内容')
                        raise IgnoredException("违规图片")
                    elif result["status"] == 'error':
                        logger.info(f"图片检测失败{result['message']}")
                    elif result["status"]:
                        logger.info(f"图片安全")
