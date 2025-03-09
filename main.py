import src.getCard
import src.postCardtools

def main():
    cardId = int(input("输入你想要制作的卡面编号: "))
    afterTraining = input("是否是训练后卡面？(y/n): ")
    cardInfo = {}
    if afterTraining == 'y':
        cardInfo = src.getCard.getCard(cardId, afterTraining=True)
    else:
        cardInfo = src.getCard.getCard(cardId, afterTraining=False)
    src.postCardtools.card2pdf(cardInfo)

if __name__ == "__main__":
    main()