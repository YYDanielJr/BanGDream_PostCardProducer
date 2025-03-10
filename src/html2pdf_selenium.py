from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import base64  # 添加 base64 模块

def html_to_pdf(html_path, output_path):
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无界面模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # 设置固定尺寸（单位：毫米）
    page_width_mm = 296
    page_height_mm = 200

    try:
        # 初始化Chrome浏览器
        # service = Service(executable_path="chromedriver/chromedriver.exe")
        driver = webdriver.Chrome(options=chrome_options)

        # 加载HTML文件
        html_absolute_path = os.path.abspath(html_path)
        driver.get(f"file:///{html_absolute_path}")

        # 注入JavaScript来隔离和缩放container元素
        # driver.execute_script("""
        #     var container = document.querySelector('.container');
        #     document.body.innerHTML = '';
        #     document.body.appendChild(container);
        #     document.body.style.margin = '0';
        #     document.body.style.padding = '0';
        #     document.documentElement.style.margin = '0';
        #     document.documentElement.style.padding = '0';
        # """)

        # 注入JavaScript来设置容器和页面样式

        # 设置打印选项
        print_options = {
            'printBackground': True,
            'landscape': False,  # 改为纵向打印
            'paperWidth': 8.7406225,  # 交换宽高
            'paperHeight': 5.905826,
            'margin': {
                'top': 0,
                'bottom': 0,
                'left': 0,
                'right': 0
            },
            'scale': 1.0,
            # 'preferCSSPageSize': True,  # 使用CSS定义的页面大小
        }
        
        # 打印为PDF并处理返回的base64数据
        result = driver.execute_cdp_cmd('Page.printToPDF', print_options)
        pdf_data = base64.b64decode(result['data'])
        
        # 保存PDF文件
        with open(output_path, 'wb') as file:
            file.write(pdf_data)
            
        print(f"PDF已成功生成: {output_path}")
        return True

    except Exception as e:
        print(f"生成PDF时出错: {str(e)}")
        return False
        
    finally:
        if 'driver' in locals():
            driver.quit()

# if __name__ == "__main__":
#     html_path = "pageTemplate/template_back.html"
#     output_path = "DocFiles/rendered.pdf"

#     html_to_pdf(html_path, output_path)