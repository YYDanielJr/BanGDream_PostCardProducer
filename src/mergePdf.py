from PyPDF2 import PdfReader, PdfWriter

def mergePdf(front_pdf, back_pdf, output_path):
    # 使用with语句确保文件正确打开和关闭
    with open(front_pdf, 'rb') as front_file, open(back_pdf, 'rb') as back_file:
        # 读取两个PDF文件
        front_reader = PdfReader(front_file)
        back_reader = PdfReader(back_file)
        
        # 创建输出PDF
        writer = PdfWriter()
        
        # 添加页面
        writer.add_page(front_reader.pages[0])
        writer.add_page(back_reader.pages[0])
        
        # 写入合并后的PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)