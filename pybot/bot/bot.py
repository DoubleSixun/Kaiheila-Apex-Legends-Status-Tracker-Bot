import json
import requests
from datetime import datetime, timedelta
from khl import Bot, Message, EventTypes, Event
from khl.card import CardMessage, Card, Module, Element, Types, Struct

with open('../config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# init Bot
bot = Bot(token=config['token'])


@bot.command(name='查询')
async def card(msg: Message, plat: str, n: str):
    print(plat, n)
    PARAMS = {"bridge": "5", "platform": plat,
              "player": n, "auth": "zH9r3XbOhZ1arWN45TBH"}
    response = requests.get(
        "https://api.mozambiquehe.re/bridge/", params=PARAMS)
    res_json = response.json()
    print(res_json["global"])

    name = res_json["global"]["name"]
    uid = res_json["global"]["uid"]
    platform = res_json["global"]["platform"]
    level = res_json["global"]["level"]
    rankName = res_json["global"]["rank"]["rankName"]
    rankDiv = res_json["global"]["rank"]["rankDiv"]
    rankScore = res_json["global"]["rank"]["rankScore"]
    rankImg = res_json["global"]["rank"]["rankImg"]

    hasDiv = 1
    if rankName == "Bronze":
        rankChineseName = "青铜"
    if rankName == "Silver":
        rankChineseName = "白银"
    if rankName == "Gold":
        rankChineseName = "黄金"
    if rankName == "Platinum":
        rankChineseName = "铂金"
    if rankName == "Diamond":
        rankChineseName = "钻石"
    if rankName == "Master":
        rankChineseName = "大师"
        hasDiv = 0
    if rankName == "Apex Predator":
        rankChineseName = "猎杀者"
        hasDiv = 0

    if hasDiv != 0:
        rank = rankChineseName + " " + str(rankDiv)
    else:
        rank = rankChineseName

    isInGame = res_json["realtime"]["isInGame"]
    if isInGame == 1:
        gameStatus = "正在游戏中"
    else:
        gameStatus = "未进行游戏"

    partyFull = res_json["realtime"]["partyFull"]
    if partyFull == 0:
        partyStatus = "未满员"
    else:
        partyStatus = "已满员"

    currentState = res_json["realtime"]["currentState"]
    if currentState == "offline":
        currentStatus = "离线"
    else:
        currentStatus = "在线"

    await msg.reply([
        {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "modules": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain-text",
                        "content": name
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "paragraph",
                        "cols": 3,
                        "fields": [
                            {
                                "type": "kmarkdown",
                                "content": "**等级**\n" + str(level)
                            },
                            {
                                "type": "kmarkdown",
                                "content": "**平台**\n" + platform
                            },
                            {
                                "type": "kmarkdown",
                                "content": "**状态**\n" + currentStatus
                            }
                        ]
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "paragraph",
                        "cols": 2,
                        "fields": [
                            {
                                "type": "kmarkdown",
                                "content": "**队伍**\n" + partyStatus
                            },
                            {
                                "type": "kmarkdown",
                                "content": "**游戏状态**\n" + gameStatus
                            }
                        ]
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "paragraph",
                        "cols": 1,
                        "fields": [
                            {
                                "type": "kmarkdown",
                                "content": "**排位赛**"
                            }
                        ]
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain-text",
                        "content": "段位: " + rank + "\n分数: " + str(rankScore)
                    }
                    # ,
                    # "mode": "right",
                    # "accessory": {
                    #     "type": "image",
                    #     "src": rankImg,
                    #     "size": "sm"
                    # }
                }
            ]
        }
    ])


@bot.command(name='地图')
async def world(msg: Message):  # when `name` is not set, the function name will be used
    map_response = requests.get(
        "https://api.mozambiquehe.re/maprotation?version=2&auth=zH9r3XbOhZ1arWN45TBH")
    map_res_json = map_response.json()
    print(map_response.text)

    curr_BY_map = map_res_json["battle_royale"]["current"]["map"]
    curr_BY_map_timer = map_res_json["battle_royale"]["current"]["remainingTimer"]
    if curr_BY_map == "Kings Canyon":
        curr_BY_map = "诸王峡谷"
    if curr_BY_map == "Olympus":
        curr_BY_map = "奥林匹斯"
    if curr_BY_map == "World's Edge":
        curr_BY_map = "世界边缘"
    if curr_BY_map == "Storm Point":
        curr_BY_map = "风暴点"

    next_BY_map = map_res_json["battle_royale"]["next"]["map"]
    if next_BY_map == "Kings Canyon":
        next_BY_map = "诸王峡谷"
    if next_BY_map == "Olympus":
        next_BY_map = "奥林匹斯"
    if next_BY_map == "World's Edge":
        next_BY_map = "世界边缘"
    if next_BY_map == "Storm Point":
        next_BY_map = "风暴点"
    await msg.reply([
        {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "modules": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain-text",
                        "content": "当前地图"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "paragraph",
                        "cols": 2,
                        "fields": [
                            {
                                "type": "kmarkdown",
                                "content": curr_BY_map
                            },
                            {
                                "type": "kmarkdown",
                                "content": "剩余时间: " + curr_BY_map_timer
                            }
                        ]
                    }
                }
            ]
        },
        {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "modules": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain-text",
                        "content": "下张地图"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain-text",
                        "content": next_BY_map
                    }
                }
            ]
        }
    ])


@bot.command(name='复制器')
async def world(msg: Message):  # when `name` is not set, the function name will be used
    craft_response = requests.get(
        "https://api.mozambiquehe.re/crafting?&auth=zH9r3XbOhZ1arWN45TBH")

    craft_res_json = craft_response.json()
    daily_item_img = []
    for item in craft_res_json[0]["bundleContent"]:
        daily_item_img.append(item["itemType"]["asset"])

    weekly_item_img = []
    for item in craft_res_json[1]["bundleContent"]:
        weekly_item_img.append(item["itemType"]["asset"])

    print(craft_response.text)
    await msg.reply([
        {
            "type": "card",
            "theme": "secondary",
            "size": "sm",
            "modules": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain-text",
                        "content": "每日轮换"
                    }
                },
                {
                    "type": "image-group",
                    "elements": [
                        {
                            "type": "image",
                            "src": daily_item_img[0]
                        },
                        {
                            "type": "image",
                            "src": daily_item_img[1]
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain-text",
                        "content": "每周轮换"
                    }
                },
                {
                    "type": "image-group",
                    "elements": [
                        {
                            "type": "image",
                            "src": weekly_item_img[0]
                        },
                        {
                            "type": "image",
                            "src": weekly_item_img[1]
                        }
                    ]
                }
            ]
        }
    ])


@bot.command(name='查询段位')
async def card(msg: Message, plat: str, n: str):
    print(plat, n)
    PARAMS = {"bridge": "5", "platform": plat,
              "player": n, "auth": "zH9r3XbOhZ1arWN45TBH"}
    response = requests.get(
        "https://api.mozambiquehe.re/bridge/", params=PARAMS)
    res_json = response.json()
    print(res_json["global"])

    name = res_json["global"]["name"]
    uid = res_json["global"]["uid"]
    platform = res_json["global"]["platform"]
    level = res_json["global"]["level"]
    rankName = res_json["global"]["rank"]["rankName"]
    rankDiv = res_json["global"]["rank"]["rankDiv"]
    rankScore = res_json["global"]["rank"]["rankScore"]
    rankImg = res_json["global"]["rank"]["rankImg"]

    hasDiv = 1
    if rankName == "Bronze":
        rankChineseName = "青铜"
    if rankName == "Silver":
        rankChineseName = "白银"
    if rankName == "Gold":
        rankChineseName = "黄金"
    if rankName == "Platinum":
        rankChineseName = "铂金"
    if rankName == "Diamond":
        rankChineseName = "钻石"
    if rankName == "Master":
        rankChineseName = "大师"
        hasDiv = 0
    if rankName == "Apex Predator":
        rankChineseName = "猎杀者"
        hasDiv = 0

    if hasDiv != 0:
        rank = rankChineseName + " " + str(rankDiv)
    else:
        rank = rankChineseName

    isInGame = res_json["realtime"]["isInGame"]
    if isInGame == 1:
        gameStatus = "正在游戏中"
    else:
        gameStatus = "未进行游戏"

    partyFull = res_json["realtime"]["partyFull"]
    if partyFull == 0:
        partyStatus = "未满员"
    else:
        partyStatus = "已满员"

    currentState = res_json["realtime"]["currentState"]
    if currentState == "offline":
        currentStatus = "离线"
    else:
        currentStatus = "在线"

    await msg.reply([
        {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "modules": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain-text",
                        "content": name
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "paragraph",
                        "cols": 3,
                        "fields": [
                            {
                                "type": "kmarkdown",
                                "content": "**等级**\n" + str(level)
                            },
                            {
                                "type": "kmarkdown",
                                "content": "**平台**\n" + platform
                            },
                            {
                                "type": "kmarkdown",
                                "content": "**状态**\n" + currentStatus
                            }
                        ]
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "paragraph",
                        "cols": 2,
                        "fields": [
                            {
                                "type": "kmarkdown",
                                "content": "**队伍**\n" + partyStatus
                            },
                            {
                                "type": "kmarkdown",
                                "content": "**游戏状态**\n" + gameStatus
                            }
                        ]
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "paragraph",
                        "cols": 1,
                        "fields": [
                            {
                                "type": "kmarkdown",
                                "content": "**排位赛**"
                            }
                        ]
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain-text",
                        "content": "段位: " + rank + "\n分数: " + str(rankScore)
                    },
                    "mode": "right",
                    "accessory": {
                        "type": "image",
                        "src": rankImg,
                        "size": "sm"
                    }
                }
            ]
        }
    ])


@bot.command(name='帮助')
async def world(msg: Message):  # when `name` is not set, the function name will be used
    await msg.reply([
        {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "modules": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain-text",
                        "content": "命令"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain-text",
                        "content": "查询基本信息:  /查询 PC/PS4/X1 你的origin名字\n                       --注: steam名字因为会重复, 所以无法查询"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain-text",
                        "content": "地图轮换:         /地图\n                       --注: 暂时只支持大逃杀模式"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain-text",
                        "content": "复制器轮换:     /复制器\n                       --注: 有时因图片无法显示而无法查询, 请稍后再试"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain-text",
                            "content": "内测版本, 仍存在不确定问题, 如有疑问请在开黑啦联系JshSdtC#3345"
                        }
                    ]
                }
            ]
        }
    ])

bot.run()
