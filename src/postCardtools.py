import os

from spire.doc import Document, DocumentObjectType, DocPicture, FileFormat
from docx2pdf import convert
import PyPDF2

def remove_page(input_pdf_path, output_pdf_path, page_number):
    # 打开PDF文件
    with open(input_pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        # 遍历所有页面，除了要删除的那一页
        for i in range(len(pdf_reader.pages)):
            if i != page_number - 1:  # 注意：页码从0开始计数，因此要减1
                pdf_writer.add_page(pdf_reader.pages[i])

        # 保存修改后的PDF文件
        with open(output_pdf_path, 'wb') as output_file:
            pdf_writer.write(output_file)

def card2pdf(cardInfo: dict):

    doc = Document()

    # 加载Word文档
    doc.LoadFromFile("./DocFiles/template.docx")

    # 创建一个列表来存储图片
    pictures = []
    #需要替换的内容
    cardPlace = "img/card_upscale.png"
    logoPlace = "TeamLogo/{}.svg".format(cardInfo["teamName"])
    sdcharaPlace = "img/pico_rgba_upscale.png"
    charaname_CN = "{}".format(cardInfo["character"][0])
    charaname_JP = "{}".format(cardInfo["character"][1])
    sentence = "{}".format(cardInfo["gachaText"][3])

    # 遍历文档中的所有节
    for i in range(doc.Sections.Count):
        sec = doc.Sections.get_Item(i)

        # 遍历每一节中的所有段落
        for j in range(sec.Paragraphs.Count):
            para = sec.Paragraphs.get_Item(j)

            # 遍历每个段落中的所有子对象
            for k in range(para.ChildObjects.Count):
                docObj = para.ChildObjects.get_Item(k)

                # 查找图片并将其添加到列表中
                if docObj.DocumentObjectType == DocumentObjectType.Picture:
                    pictures.append(docObj)

    #改卡面
    card = DocPicture(pictures[0])
    width = card.Width
    height = card.Height
    card.LoadImage(cardPlace)
    card.Width = width
    card.Height = height

    #改队标
    logo = DocPicture(pictures[1])
    width = logo.Width
    height = logo.Height
    logo.LoadImage(logoPlace)
    logo.Width = width
    logo.Height = height

    #改小人
    sdchara = DocPicture(pictures[2])
    width = sdchara.Width
    height = sdchara.Height
    sdchara.LoadImage(sdcharaPlace)
    sdchara.Width = width
    sdchara.Height = height

    #改文案
    doc.Replace("山吹 沙绫", charaname_CN, False, True)
    doc.Replace("SAAYA YAMABUKI",charaname_JP,False, True)
    doc.Replace("你又这么 轻易地答应了……",sentence,False, True)
    # 保存结果文档
    doc.SaveToFile("./DocFiles/Output.docx")
    doc.Close()

    convert("./DocFiles/Output.docx")

    input_pdf = 'DocFiles/Output.pdf'  # 原始PDF文件路径
    output_pdf = 'DocFiles/Postcard.pdf'  # 修改后的PDF文件路径
    page_to_remove = 1  # 要删除的页码（例如，第2页）
    remove_page(input_pdf, output_pdf, page_to_remove)

    os.remove("DocFiles/Output.pdf")

    print("Done")



# 使用示例
# input_pdf = 'DocFiles/Output.pdf'  # 原始PDF文件路径
# output_pdf = 'DocFiles/Postcard.pdf'  # 修改后的PDF文件路径
# page_to_remove = 1  # 要删除的页码（例如，第2页）
# remove_page(input_pdf, output_pdf, page_to_remove)

# os.remove("DocFiles/Output.pdf")

# print("Done")