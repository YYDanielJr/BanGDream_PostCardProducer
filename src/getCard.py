import json
import os
from bestdori.cards import Card
from bestdori.costumes import Costume

from PIL import Image

import subprocess
# from RealESRGAN import RealESRGAN
# import torch

characerMap = {
    1: ["户山 香澄", "TOYAMA KASUMI", "户山香澄", "kasumi"],
    2: ["花园 多惠", "HANAZONO TAE", "花园多惠", "tae"],
    3: ["牛込 里美", "USHIGOME RIMI", "牛込里美", "rimi"],
    4: ["山吹 沙绫", "YAMABUKI SĀYA", "山吹沙绫", "saya"],
    5: ["市谷 有咲", "ICHIGAYA ARISA", "市谷有咲", "arisa"],
    6: ["美竹 兰", "MITAKE RAN", "美竹兰", "ran"],
    7: ["青叶 摩卡", "AOBA MOCA", "青叶摩卡", "moca"],
    8: ["上原 绯玛丽", "UEHARA HIMARI", "上原绯玛丽", "himari"],
    9: ["宇田川 巴", "UDAGAWA TOMOE", "宇田川巴", "tomoe"],
    10: ["羽泽 鸫", "HAZAWA TSUGUMI", "羽泽鸫", "tsugumi"],
    11: ["弦卷 心", "TSURUMAKI KOKORO", "弦卷心", "kokoro"],
    12: ["濑田 薰", "SETA KAORU", "濑田薰", "kaoru"],
    13: ["北泽 育美", "KITAZAWA HAGUMI", "北泽育美", "hagumi"],
    14: ["松原 花音", "MATSUBARA KANON", "松原花音", "kanon"],
    15: ["奥泽 美咲", "OKUSAWA MISAKI", "奥泽美咲", "misaki"],
    16: ["丸山 彩", "MARUYAMA AYA", "丸山彩", "aya"],
    17: ["冰川 日菜", "HIKAWA HINA", "冰川日菜", "hina"],
    18: ["白鹭 千圣", "SHIRASAGI CHISATO", "白鹭千圣", "chisato"],
    19: ["大和 麻弥", "YAMATO MAYA", "大和麻弥", "maya"],
    20: ["若宫 伊芙", "WAKAMIYA EVE", "若宫伊芙", "eve"],
    21: ["凑 友希那", "MINATO YUKINA", "凑友希那", "yukina"],
    22: ["冰川 纱夜", "HIKAWA SAYO", "冰川纱夜", "sayo"],
    23: ["今井 莉莎", "IMAI LISA", "今井莉莎", "lisa"],
    24: ["宇田川 亚子", "UDAGAWA AKO", "宇田川亚子", "ako"],
    25: ["白金 燐子", "SHIROKANE RINKO", "白金燐子", "rinko"],
    26: ["仓田 真白", "KURATA MASHIRO", "仓田真白", "mashiro"],
    27: ["桐谷 透子", "KIRIGAYA TOKO", "桐谷透子", "toko"],
    28: ["广町 七深", "HIROMACHI NANAMI", "广町七深", "nanami"],
    29: ["二叶 筑紫", "FUTABA TSUKUSHI", "二叶筑紫", "tsukushi"],
    30: ["八潮 瑠唯", "YASHIO RUI", "八潮瑠唯", "rui"],
    31: ["和奏 瑞依/LAYER", "WAKANA REI", "和奏瑞依", "layer"],
    32: ["朝日 六花/LOCK", "ASAHI ROKKA", "朝日六花", "lock"],
    33: ["佐藤 益木/MASKING", "SATOU MASUKI", "佐藤益木", "masking"],
    34: ["鳰原 令王那/PAREO", "NYUBARA REONA", "鳰原令王那", "pareo"],
    35: ["珠手 知由/CHU²", "TAMADE CHIYU", "珠手知由", "chu²"],
    36: ["高松 灯", "TAKAMATSU TOMORI", "高松灯", "tomori"],
    37: ["千早 爱音", "CHIHAYA ANON", "千早爱音", "anon"],
    38: ["要 乐奈", "KANAME RĀNA", "要乐奈", "rana"],
    39: ["长崎 爽世", "NAGASAKI SOYO", "长崎爽世", "soyo"],
    40: ["椎名 立希", "SHIINA TAKI", "椎名立希", "taki"]
}

def getCard(cardId, afterTraining=False):

    current_work_dir = os.getcwd()
    print(current_work_dir)
    card = Card(cardId)
    if afterTraining:
        png = card.get_card(type='after_training')
    else:
        png = card.get_card(type='normal')

    with open("img/card.png", 'wb') as f:
        f.write(png)

    all = card.get_info()

    gachaText = all['gachaText']
    for i in range(0, 5):
        if gachaText[i]:
            gachaText[i] = gachaText[i].replace("\n", " ")

    characterId = all['characterId']

    cardInfo = {
        "character": characerMap[characterId],
        "title": all['prefix'],
        "gachaText": gachaText,
    }

    if characterId >= 1 and characterId <= 5:
        cardInfo["teamName"] = "ppp"
    elif characterId >= 6 and characterId <= 10:
        cardInfo["teamName"] = "ag"
    elif characterId >= 11 and characterId <= 15:
        cardInfo["teamName"] = "hhw"
    elif characterId >= 16 and characterId <= 20:
        cardInfo["teamName"] = "paspale"
    elif characterId >= 21 and characterId <= 25:
        cardInfo["teamName"] = "roselia"
    elif characterId >= 26 and characterId <= 30:
        cardInfo["teamName"] = "monica"
    elif characterId >= 31 and characterId <= 35:
        cardInfo["teamName"] = "ras"
    elif characterId >= 36 and characterId <= 40:
        cardInfo["teamName"] = "mygo"
    else:
        pass

    costumeId = all['costumeId']
    costume = Costume(costumeId)
    pico = costume.get_icon()

    with open("img/pico.png", 'wb') as f:
        f.write(pico)

    pico_rgba = Image.open("img/pico.png").convert("RGBA")
    pico_rgba.save("img/pico_rgba.png", "PNG")

    ret1 = subprocess.run(["realesrgan/realesrgan-ncnn-vulkan", "-i", "img/pico_rgba.png", "-o", "img/pico_rgba_upscale.png", "-n", "realesrgan-x4plus-anime"])
    ret2 = subprocess.run(["realesrgan/realesrgan-ncnn-vulkan", "-i", "img/card.png", "-o", "img/card_upscale.png", "-n", "realesrgan-x4plus-anime"])

    return cardInfo