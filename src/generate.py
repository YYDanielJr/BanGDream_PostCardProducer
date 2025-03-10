from bs4 import BeautifulSoup
import requests

def generateHtml(cardInfo: dict):
    # 读取前面页的HTML和CSS
    with open("pageTemplate/template_front.html", "r", encoding="utf-8") as f:
        html = f.read()
    with open("pageTemplate/style_front.css", "r", encoding="utf-8") as f:
        css = f.read()
    
    # 解析HTML
    soup = BeautifulSoup(html, "html.parser")
    
    # 创建style标签并添加CSS内容
    style = soup.new_tag("style")
    style.string = css
    
    # 将style标签添加到head中
    head = soup.find("head")
    if head:
        # 删除原有的link标签
        for link in head.find_all("link", rel="stylesheet"):
            link.decompose()
        # 添加新的style标签
        head.append(style)

    englishName = soup.find("p", id="english-content")
    englishName.string = cardInfo["character"][1]

    chineseName = soup.find("p", id="chinese-content")
    chineseNameStrings = cardInfo["character"][0].split("/")
    if len(chineseNameStrings) == 1:
        chineseName.string = chineseNameStrings[0]
    else:
        chineseName.clear()  # 清除原有内容
        name_text = soup.new_string(chineseNameStrings[0])
        slash = soup.new_tag("span", attrs={"class": "slash"})
        slash.string = "/"
        after_slash = soup.new_tag("span", attrs={"class": "after-slash"})
        after_slash.string = chineseNameStrings[1]

        chineseName.append(name_text)
        chineseName.append(slash)
        chineseName.append(after_slash)

    mainImage = soup.find("img", id="main-card-image")
    mainImage["src"] = "../img/card_upscale.png"

    teamLogo = soup.find("img", class_="team-logo")
    teamLogo["src"] = f"../TeamLogo/{cardInfo['teamName']}.svg"

    with open("cache/front.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    # 读取背面页的HTML和CSS
    with open("pageTemplate/template_back.html", "r", encoding="utf-8") as f:
        html = f.read()
    with open("pageTemplate/style_back.css", "r", encoding="utf-8") as f:
        css = f.read()

    soup = BeautifulSoup(html, "html.parser")
    
    # 创建style标签并添加CSS内容
    style = soup.new_tag("style")
    style.string = css
    
    # 将style标签添加到head中
    head = soup.find("head")
    if head:
        # 删除原有的link标签
        for link in head.find_all("link", rel="stylesheet"):
            link.decompose()
        # 添加新的style标签
        head.append(style)

    note = soup.find("div", class_="note")
    if cardInfo["gachaText"][3]:
        note.string = "『" + cardInfo["gachaText"][3] + "』"
    elif cardInfo["title"][3]:
        note.string = "『" + cardInfo["title"][3] + "』"
    else:
        note.string = " "

    pico = soup.find("img", class_="character-png")
    pico["src"] = "../img/pico_rgba_upscale.png"

    with open("cache/back.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())