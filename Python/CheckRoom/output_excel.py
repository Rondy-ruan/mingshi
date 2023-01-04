import xlsxwriter

workbook = xlsxwriter.Workbook('测试文件11.xlsx')
worksheet = workbook.add_worksheet('这是sheet1')
format_1 = {
    'font_name' : '楷体', # 字体
    'font_size': 20,  # 字体大小
    'font_color': 'black',  # 字体颜色
    'bold': True,  # 是否粗体
    'bg_color': '#101010',  # 表格背景颜色
    'fg_color': '#00FF00',  # 前景颜色
    'align': 'center',  # 水平居中对齐
    'valign': 'vcenter',  # 垂直居中对齐
    # 'num_format': 'yyyy-mm-dd H:M:S',# 设置日期格式
    # 后面参数是线条宽度
    'border': 0,  # 边框宽度
    'top': 0,  # 上边框
    
    'left': 0,  # 左边框
    'right': 0,  # 右边框
    'bottom': 0  # 底边框
}


format_2 = {
    'font_name' : '楷体', # 字体
    'font_size': 16,  # 字体大小
    'font_color': 'black',  # 字体颜色
    'bold': True,  # 是否粗体
    'bg_color': '#101010',  # 表格背景颜色
    'fg_color': '#00FF00',  # 前景颜色
    'align': 'left',  # 水平居中对齐
    'valign': 'vcenter',  # 垂直居中对齐
    # 'num_format': 'yyyy-mm-dd H:M:S',# 设置日期格式
    # 后面参数是线条宽度
    'border': 0,  # 边框宽度
    'top': 0,  # 上边框
    
    'left': 0,  # 左边框
    'right': 0,  # 右边框
    'bottom': 5  # 底边框
}

format_3 = {
    'font_name' : '楷体', # 字体
    'font_size': 16,  # 字体大小
    'font_color': 'black',  # 字体颜色
    'bold': True,  # 是否粗体
    'bg_color': '#101010',  # 表格背景颜色
    'fg_color': '#00FF00',  # 前景颜色
    'align': 'left',  # 水平居中对齐
    'valign': 'vn',  # 垂直居中对齐
    # 'num_format': 'yyyy-mm-dd H:M:S',# 设置日期格式
    # 后面参数是线条宽度
    'border': 0,  # 边框宽度
    'top': 0,  # 上边框
    
    'left': 0,  # 左边框
    'right': 0,  # 右边框
    'bottom': 0  # 底边框
}

format_4 = {
    'font_name' : '楷体', # 字体
    'font_size': 12,  # 字体大小
    'font_color': 'black',  # 字体颜色
    'bold': False,  # 是否粗体
    'bg_color': '#101010',  # 表格背景颜色
    'fg_color': '#00FF00',  # 前景颜色
    'align': 'center',  # 水平居中对齐
    'valign': 'vcenter',  # 垂直居中对齐
    # 'num_format': 'yyyy-mm-dd H:M:S',# 设置日期格式
    # 后面参数是线条宽度
    'border': 0,  # 边框宽度
    'top': 0,  # 上边框
    
    'left': 0,  # 左边框
    'right': 0,  # 右边框
    'bottom': 0  # 底边框
}


format_5 = {
    'font_name' : '楷体', # 字体
    'font_size': 14,  # 字体大小
    'font_color': 'black',  # 字体颜色
    'bold': False,  # 是否粗体
    'bg_color': '#101010',  # 表格背景颜色
    'fg_color': '#00FF00',  # 前景颜色
    'align': 'center',  # 水平居中对齐
    'valign': 'vcenter',  # 垂直居中对齐
    # 'num_format': 'yyyy-mm-dd H:M:S',# 设置日期格式
    # 后面参数是线条宽度
    'border': 0,  # 边框宽度
    'top': 0,  # 上边框
    
    'left': 0,  # 左边框
    'right': 0,  # 右边框
    'bottom': 0  # 底边框
}

format_6 = {
    'font_name' : '楷体', # 字体
    'font_size': 12,  # 字体大小
    'font_color': 'black',  # 字体颜色
    'bold': False,  # 是否粗体
    'bg_color': '#101010',  # 表格背景颜色
    'fg_color': '#00FF00',  # 前景颜色
    'align': 'e',  # 水平居中对齐
    'valign': 'vcenter',  # 垂直居中对齐
    # 'num_format': 'yyyy-mm-dd H:M:S',# 设置日期格式
    # 后面参数是线条宽度
    'border': 0,  # 边框宽度
    'top': 0,  # 上边框
    
    'left': 0,  # 左边框
    'right': 0,  # 右边框
    'bottom': 0  # 底边框
}

format_7 = {
    'font_name' : '楷体', # 字体
    'font_size': 16,  # 字体大小
    'font_color': 'black',  # 字体颜色
    'bold': True,  # 是否粗体
    'bg_color': '#101010',  # 表格背景颜色
    'fg_color': '#00FF00',  # 前景颜色
    'align': 'center',  # 水平居中对齐
    'valign': 'vn',  # 垂直居中对齐
    # 'num_format': 'yyyy-mm-dd H:M:S',# 设置日期格式
    # 后面参数是线条宽度
    'border': 0,  # 边框宽度
    'top': 0,  # 上边框
    
    'left': 0,  # 左边框
    'right': 0,  # 右边框
    'bottom': 0  # 底边框
}

# 设置行宽
worksheet.set_row(0, 33)# 第一行行宽


worksheet.set_row(6, 138)

# 设置列宽
worksheet.set_column('A:A', 19)
worksheet.set_column('B:B', 12)
worksheet.set_column('C:C', 14)
worksheet.set_column('D:D', 2)
worksheet.set_column('E:E', 19)
worksheet.set_column('F:F', 12)
worksheet.set_column('G:G', 24)

style_1 = workbook.add_format(format_1)  # 设置样式format是一个字典
style_2 = workbook.add_format(format_2)
style_3 = workbook.add_format(format_3)
style_4 = workbook.add_format(format_4)
style_5 = workbook.add_format(format_5)
style_6 = workbook.add_format(format_6)
style_7 = workbook.add_format(format_7)

str_a1 = '生理状态检查表（病历）'
worksheet.merge_range('A1:G1', str_a1, style_1)

str_a2 = '客户编号：0000012'
str_g2 = '第1次'

worksheet.merge_range('A2:C2', str_a2, style_2)
worksheet.write('G2', str_g2, style_2)
worksheet.write('D2', '', style_2)
worksheet.write('E2', '', style_2)
worksheet.write('F2', '', style_2)

str_a3 = '姓名：牙毅'
str_c3 = '性别：男'
str_e3 = '年龄：37'
str_f3 = '电话：'
worksheet.merge_range('A3:B3', str_a3, style_3)
worksheet.write('C3', str_c3, style_3)
worksheet.write('E3', str_e3, style_3)
worksheet.merge_range('F3:G3', str_f3, style_3)

str_a4 = '以往状态：'
str_b4 = '轻微头晕症状、疲惫状态'
worksheet.write('A4', str_a4, style_2)
worksheet.merge_range('B4:G4', '', style_2)
worksheet.write('B4', str_b4, style_2)

sta_a5 = '理疗前状态'
str_e5 = '理疗后状态'
worksheet.merge_range('A5:C5', sta_a5, style_7)
worksheet.merge_range('E5:G5', str_e5, style_7)


str_a6 = '时间：2021年01月11日 12时02分44秒'
str_e6 = '时间：2021年01月11日 14时08分40秒'
worksheet.merge_range('A6:C6', str_a6, style_4)
worksheet.merge_range('E6:G6', str_e6, style_4)

img_a7 = './package/l.png'
img_e7 = './package/r.png'
worksheet.insert_image('A7', img_a7)
worksheet.insert_image('E7', img_a7)

for i in range(7,23):
        worksheet.merge_range(i, 1, i, 2, "")
for i in range(7,23):
        worksheet.merge_range(i, 5, i, 6, "")

line_str_a8_a13 = ["体重：","补充：","收缩压：","扩张压：","心率：","血糖："]
for i in range(0,6):
     worksheet.write(7+i, 0, line_str_a8_a13[i], style_5)   
for i in range(0,6):
     worksheet.write(7+i, 4, line_str_a8_a13[i], style_5)  

str_a14 = str_e14 = '其他：'
worksheet.write('A14', str_a14, style_4)
worksheet.write('E14', str_e14, style_4)

line_str_a15_a22 = ["身高：", "体脂：", "水分：", "肌肉值：", "骨骼量：", "卡路里：", "BMI值：", "脉搏：", "血氧："]
for i in range(0,9):
     worksheet.write(14+i, 0, line_str_a15_a22[i], style_6)  
for i in range(0,9):
     worksheet.write(14+i, 4, line_str_a15_a22[i], style_6)  
worksheet.merge_range('A24:G24', '', style_2)

str_a25 ='效果、医嘱：'
worksheet.write('A25', str_a25, style_3)
str_a26 = '体重：-0.4 Kg  排汗（毒）：+1.15 Kg  血糖：0 mmol/l  '
worksheet.merge_range('A26:G26', str_a26, style_3)
str_a27 = '收缩压：-5 mmHg  扩张压：-13 mmHg'
worksheet.merge_range('A27:G27', str_a27, style_3)
str_a28 = '面色红润、状态佳；头晕状况减轻，'
worksheet.merge_range('A28:G28', str_a28, style_3)
str_a29 = '理疗技师:'
worksheet.merge_range('A29:B29', str_a29, style_3)
str_c29 = '颜永珊'
worksheet.write('C29', str_c29, style_3)
str_e29 = '商业卫生服务站'
worksheet.merge_range('E29:F29', str_e29, style_3)
str_g29 = '高血压理疗科'
worksheet.write('G29', str_g29, style_3)

workbook.close()
