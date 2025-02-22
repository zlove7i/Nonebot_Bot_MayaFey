# Nonebot_Bot_MayaFey
## 本项目
基于[Nonebot2](https://https://v2.nonebot.dev/)和[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)制作的群聊机器人

## 适配
目前只适配了 go-cqhttp,有兴趣的可以自己尝试其他 Onebot,但请自行承担可能存在的兼容性问题  
机器人所有的功能(除部分私聊功能外)都只适配了群聊,不保证私聊情况下能正常使用

## 名称来源
该项目名称来自 [逆转裁判](https://baike.baidu.com/item/%E9%80%86%E8%BD%AC%E8%A3%81%E5%88%A4/56352) 中的 [绫里真宵](https://baike.baidu.com/item/%E7%BB%AB%E9%87%8C%E7%9C%9F%E5%AE%B5/733281)

## 文档地址
[点击这里](https://mayafey.shinelight.xyz)

## 声明
1. 由于QQ是不允许第三方机器人存在的,所以在使用过程中可能会出现账号被风控、被冻结、被封号等情况,在使用前请自行权衡,开发者不对这些情况负责  
2. 该项目旨在学习和提供参考,禁止用于非法用途和盈利  
3. 该项目纯兴趣开发,开发者现在高中在读,学业限制,开发进度缓慢  
4. 本人技术一般,代码写的不咋地,还请各位大佬手下留情  
5. 遇到bug请及时提Issue,有时间了我就会修复,欢迎pr
6. 机器人的插件可以自己扒下来用,但请保留开发者信息
7. 若该项目有任何地方有侵犯到你的权益请立即联系我 `shine_light@qq.com`
8. 你的支持是我最大的动力,喜欢的话给个star吧 ~~求求了~~

## 更新日志
[更新日志](https://mayafey.shinelight.xyz/updatelog)

## 吹水群
[622945924](https://jq.qq.com/?_wv=1027&k=ElDdjklL)

## 功能
<details>
<summary>已实现的功能</summary>

### 帮助功能  
- [X] 菜单
- [X] 插件帮助 ([nonebot-plugin-help](https://github.com/XZhouQD/nonebot-plugin-help)修改而来)
### 娱乐功能
- [X] 签到  
- [X] 积分  
- [X] 一言  
- [X] 随机二次元  
- [X] 全网热搜榜    
- [X] 点歌台 ([nonebot-plugin-simplemusic](https://github.com/noneplugin/nonebot-plugin-simplemusic)修改而来)  
- [X] 群词云  ([nonebot_plugin_admin](https://github.com/yzyyz1387/nonebot_plugin_admin)修改而来)   
- [X] 头像表情包制作  ([nonebot-plugin-memes](https://github.com/noneplugin/nonebot-plugin-memes)修改而来)
- [X] 答案之书  ([nonebot-plugin-answersbook](https://github.com/A-kirami/nonebot-plugin-answersbook)修改而来)
- [X] 到账语音生成  
- [X] 今日运势  ([nonebot_plugin_fortune](https://github.com/MinatoAquaCrews/nonebot_plugin_fortune)修改而来)  
- [X] 发言排行榜  ([nonebot_plugin_admin](https://github.com/yzyyz1387/nonebot_plugin_admin)修改而来)
- [X] AI聊天  
- [X] 折磨群友  
- [X] 模拟原神祈愿  (基于[GenshinPray](https://github.com/GardenHamster/GenshinPray))
- [X] 原神角色展柜 ([nonebot-plugin-gspanel](https://github.com/monsterxcn/nonebot-plugin-gspanel))
- [X] 随机群友老婆 
### 生活功能
- [X] 腾讯翻译  ([nonebot_plugin_translator](https://github.com/Lancercmd/nonebot_plugin_translator)修改而来) 
- [X] 百度翻译  ([nonebot_plugin_baidutranslate](https://github.com/NumberSir/nonebot_plugin_baidutranslate)修改而来)  
- [X] 天气  ([nonebot-plugin-heweather](https://github.com/kexue-z/nonebot-plugin-heweather)修改而来)  
- [X] Epic喜加一  ([nonebot_plugin_epicfree](https://github.com/monsterxcn/nonebot_plugin_epicfree)修改而来)  
- [X] 吃什么  ([nonebot_plugin_what2eat](https://github.com/MinatoAquaCrews/nonebot_plugin_what2eat)修改而来)  
- [X] 早晚安  ([nonebot_plugin_morning](https://github.com/MinatoAquaCrews/nonebot_plugin_morning)修改而来)   
### 群聊管理功能
- [X] 机器人更新 
- [X] 重启  
- [X] 机器人开关  
- [X] 群管
- [X] 违禁词
- [X] 插件控制  
- [X] 插件统计 
- [X] 增删问答   
- [X] 记过
- [X] 自定义定时任务
- [X] 入群欢迎
- [X] 离群提示
- [X] 宵禁
### 私聊管理功能
- [X] SQL查询  
- [X] 机器人好友请求管理
- [X] 控制机器人发送群聊信息
### 权限系统
- [X] 权限检测(被动)  
- [X] 查看权限  
- [X] 设置权限  
### 游戏功能
- [X] 俄罗斯轮盘  ([nonebot_plugin_russian](https://github.com/HibiKier/nonebot_plugin_russian)修改而来)  
- [X] 21点  ([nonebot-plugin-blackjack](https://github.com/yaowan233/nonebot-plugin-blackjack)修改而来)  
- [X] 猜群友
### 被动功能
- [X] 恶意触发命令检测  
- [X] 违禁图片检测(百度和腾讯接口)  
- [X] 拉群自接受  
- [X] 好友自接受  
- [X] 复读  
- [X] 定时撤回  
- [X] 防白嫖  
</details>

## UI
[Nonebot_Bot_MayaFey_UI](https://github.com/Shine-Light/Nonebot_Bot_MayaFey_UI)

## WebUI
[mayafey_webui](https://github.com/Shine-Light/mayafey_webui)

## 未来可能增加的功能
- [ ] Docker容器部署
- [ ] 更多的功能
- [x] 可视化界面

## 感谢
[Onebot](https://github.com/botuniverse/onebot-11)  
[Nonebot](https://github.com/nonebot/nonebot2)  
[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)  
[htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender)  
以及各位插件开发者

## License
[MIT License](https://opensource.org/licenses/MIT)
