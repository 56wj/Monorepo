import xlwings as xw
import commen
import shutil
import json


def generator_excel(json_data, source_path, target_path, OrderId, tray_size):
    base = "货柜"
    content_base_idx = 6
    # 复制源文件
    try:
        shutil.copy(source_path, target_path)
    except Exception as e:
        print(f"复制文件时发生错误: {e}")
    app = xw.App(visible=False)  # 设置为True可以在修改过程中看到 Excel 界面
    workbook = app.books.open(target_path)
    try:
        # 复制Sheet
        idx = 0
        for _, item in enumerate(json_data):
            if "bin_item" in item:
                idx += 1
                num_tray = json_data[item]["whole_tray_number"]
                if str(num_tray) in [sheet.name for sheet in workbook.sheets]:
                    copy_sheet = workbook.sheets[str(num_tray)]
                    copy_sheet.api.Copy(Before=copy_sheet.api)
                    new_sheet = workbook.sheets[str(num_tray) + ' (2)']  # Excel 默认的复制命名方式
                    new_sheet.name = base + str(idx)
                else:
                    print("没有此规格的模板")

        # 修改数值
        idx = 0
        for _,item in enumerate(json_data):
            if "bin_item" in item:
                idx += 1
                sheet = workbook.sheets[base + str(idx)]
                # 修改基础值
                sheet.range("B3").value = OrderId
                sheet.range("G4").value = tray_size

                # 修改货物数据
                excel_data = json_data[item]["excel_data"]
                for line , row in enumerate(excel_data):
                    row_data = excel_data[row]
                    # 修改编号
                    sheet.range("A"+str(content_base_idx + line)).value = row_data["no"]
                    # 修改厚度
                    sheet.range("B"+str(content_base_idx + line)).value = row_data["thickness"]
                    # 修改宽度
                    sheet.range("C"+str(content_base_idx + line)).value = row_data["width"]
                    # 修改卷数
                    sheet.range("D"+str(content_base_idx + line)).value = row_data["number"]

        # 删除sheet
        for sheet_name in workbook.sheet_names:
            if base not in sheet_name:
                sheet = workbook.sheets[sheet_name]
                sheet.delete()
    except Exception as e:
        print(f"在操作 Excel 时发生错误：{e}")

    finally:
        # 关闭工作簿和 Excel 应用，确保释放资源
        if workbook:
            workbook.close()
        app.quit()


if __name__ == "__main__":
    # 示例用法
    source_file_path = 'export_template.xlsx'
    cell_address = 'B6'
    with open('output.json', 'r', encoding='utf-8') as file:
        json_second_data = json.load(file)
    json_data = commen.json_data
    generator_excel(json_data, source_file_path, "/temp1.xlsx", "111", "11*12")
