import os
import src.getCard
import src.generate
import src.html2pdf_selenium
import src.mergePdf

def main():
    cardId = int(input("输入你想要制作的卡面编号: "))
    afterTraining = input("是否是训练后卡面？(y/n): ")
    cardInfo = {}
    try:
        if afterTraining == 'y':
            cardInfo = src.getCard.getCard(cardId, afterTraining=True)
        else:
            cardInfo = src.getCard.getCard(cardId, afterTraining=False)
        os.makedirs("cache", exist_ok=True)
        src.generate.generateHtml(cardInfo)
        src.html2pdf_selenium.html_to_pdf("cache/front.html", "cache/front.pdf")
        src.html2pdf_selenium.html_to_pdf("cache/back.html", "cache/back.pdf")

        os.makedirs("output", exist_ok=True)
        src.mergePdf.mergePdf("cache/front.pdf", "cache/back.pdf", "output/{}_{}.pdf".format(cardInfo["characterChineseName"], cardId))
    except Exception as e:
        print(f"生成明信片出错: {str(e)}")

if __name__ == "__main__":
    main()