import math
import os
import textwrap
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from rectpack import newPacker, MaxRectsBl, GuillotineBlsfSas, MaxRectsBlsf, MaxRectsBaf, MaxRectsBssf, MaxRectsBbef, MaxRectsBiof
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font
from datetime import datetime
from path_utils import get_static_images_dir, build_asset_path

# 设置字体（SimHei 是一个常用的支持中文的字体，可以替换为你系统中的其他字体）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def list_add_item(material_list, item_json):
    for item in material_list:
        if item['name'] == item_json['name'] and item['size'] == item_json['size']:
            item['number'] += item_json['number']
            return 0
    material_list.append(item_json)
    return 0


def color_gradient(value):
    """
    根据给定的值生成从红到黄之间的颜色。
    返回:
        str: 16进制颜色值。
    """
    if not (0 <= value <= 1):
        raise ValueError("输入值必须在 0 到 1 之间")

    # 红色和黄色的 RGB 值
    red = 255
    green = int(255 * value)  # 线性插值计算绿色值，0 -> 255

    # 将RGB值转换为16进制颜色
    hex_color = f'#{red:02X}{green:02X}00'  # 蓝色分量始终为 00

    return hex_color


def _unique_sorted(values, eps=1e-6):
    values = sorted(values)
    unique_values = []
    for value in values:
        if not unique_values or abs(value - unique_values[-1]) > eps:
            unique_values.append(value)
    return unique_values


def analyze_enclosed_holes(bin_width, bin_length, placed_items):
    x_coords = [0, bin_width]
    y_coords = [0, bin_length]
    rectangles = []

    for item in placed_items:
        left = max(0, item["position_x"])
        bottom = max(0, item["position_y"])
        right = min(bin_width, left + item["length"])
        top = min(bin_length, bottom + item["width"])
        if right <= left or top <= bottom:
            continue
        rectangles.append((left, bottom, right, top))
        x_coords.extend([left, right])
        y_coords.extend([bottom, top])

    xs = _unique_sorted(x_coords)
    ys = _unique_sorted(y_coords)
    column_count = len(xs) - 1
    row_count = len(ys) - 1

    if column_count <= 0 or row_count <= 0:
        return {"has_enclosed_hole": False, "enclosed_hole_area": 0}

    occupied = [[False] * column_count for _ in range(row_count)]
    for row in range(row_count):
        cy = (ys[row] + ys[row + 1]) / 2
        for col in range(column_count):
            cx = (xs[col] + xs[col + 1]) / 2
            for left, bottom, right, top in rectangles:
                if left <= cx < right and bottom <= cy < top:
                    occupied[row][col] = True
                    break

    visited = [[False] * column_count for _ in range(row_count)]
    queue = []

    def enqueue(row, col):
        if row < 0 or row >= row_count or col < 0 or col >= column_count:
            return
        if occupied[row][col] or visited[row][col]:
            return
        visited[row][col] = True
        queue.append((row, col))

    for col in range(column_count):
        enqueue(0, col)
        enqueue(row_count - 1, col)
    for row in range(row_count):
        enqueue(row, 0)
        enqueue(row, column_count - 1)

    head = 0
    while head < len(queue):
        row, col = queue[head]
        head += 1
        enqueue(row - 1, col)
        enqueue(row + 1, col)
        enqueue(row, col - 1)
        enqueue(row, col + 1)

    enclosed_hole_area = 0
    for row in range(row_count):
        for col in range(column_count):
            if not occupied[row][col] and not visited[row][col]:
                enclosed_hole_area += (xs[col + 1] - xs[col]) * (ys[row + 1] - ys[row])

    return {
        "has_enclosed_hole": enclosed_hole_area > 0,
        "enclosed_hole_area": round(enclosed_hole_area, 2)
    }


def create_material_excel(material_list, task_id, order_id, date, algo_name):
    # 创建一个新的工作簿
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "辅材需求单"

    # 设置表头
    headers = ["品名", "规格", "单位", "数量", "到货日期", "备注"]

    # 插入标题
    sheet.merge_cells('A1:F1')
    sheet['A1'] = "辅材需求单"
    sheet['A1'].alignment = Alignment(horizontal='center', vertical='center')
    sheet['A1'].font = Font(size=14, bold=True)

    # 插入订单号和日期
    sheet['A2'] = f"订单号:{order_id}"
    sheet.merge_cells('A2:B2')
    sheet['E2'] = f"日期:{datetime.now().date()}"
    sheet.merge_cells('E2:F2')

    # 插入表头
    for col_num, header in enumerate(headers, 1):
        cell = sheet.cell(row=3, column=col_num)
        cell.value = header
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.font = Font(bold=True)

    for row_num, row_data in enumerate(material_list, 4):
        for col_num, value in enumerate(row_data, 1):
            cell = sheet.cell(row=row_num, column=col_num)
            cell.value = row_data[value]
            cell.alignment = Alignment(horizontal='center', vertical='center')
        cell = sheet.cell(row=row_num, column=5)
        cell.value = date[0:10]
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # 插入申请人和审批人
    row_num += 1
    sheet.merge_cells(f'A{row_num}:B{row_num}')
    sheet[f'A{row_num}'] = "申请人:"
    cell = sheet.cell(row=row_num, column=1)
    cell.alignment = Alignment(horizontal='left', vertical='center')
    sheet.merge_cells(f'E{row_num}:F{row_num}')
    sheet[f'E{row_num}'] = "审批人:"
    cell = sheet.cell(row=row_num, column=5)
    cell.alignment = Alignment(horizontal='left', vertical='center')

    # 自动调整列宽
    for col_num in range(1, len(headers) + 1):
        column_letter = get_column_letter(col_num)
        sheet.column_dimensions[column_letter].width = 15

    # 构造保存路径
    save_dir = os.path.join(get_static_images_dir(), task_id, algo_name)

    # 创建目录（如果不存在）
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 构造完整的保存路径
    save_path = os.path.join(save_dir, '辅材需求单.xlsx')

    # 保存Excel文件
    workbook.save(save_path)
    print(f"Excel文件已保存到: {save_path}")
    print("Excel文件已生成!")
    save_path = build_asset_path('images', task_id, algo_name, '辅材需求单.xlsx')
    return save_path


class SuspendPack:
    def __init__(self, json_data, truck_size_data, task_id, arrive_date, tube_size_data):
        self.bin_list = []
        self.bin_list_with_n = []
        self.arrive_date = arrive_date
        self.tray_kind = json_data['config']['tray']
        bin_id = [item['box_id'] for item in json_data['config']['box_list']]
        bin_number = [item['num'] for item in json_data['config']['box_list']]
        bin_min_height = 1000
        tubeApproximate = 0
        for tube_data in tube_size_data["data"]:
            if tube_data["id"] == json_data['config']['tubeId']:
                tubeApproximate = tube_data["tubeApproximate"]
                break

        # 对照id 加入车厢
        for i in range(len(bin_id)):
            for j in range(len(truck_size_data['data'])):
                if bin_id[i] == truck_size_data['data'][j]['id']:
                    bin_name = truck_size_data['data'][j]['name']
                    bin_length = truck_size_data['data'][j]['lengthM'] * 100
                    bin_width = truck_size_data['data'][j]['widthM'] * 100
                    bin_height = truck_size_data['data'][j]['heightM'] * 100
                    bin_min_height = min(bin_min_height, bin_height)
                    bin_max_weight = truck_size_data['data'][j]['weightT']
                    self.bin_list.append((bin_width, bin_length, bin_number[i], bin_height, bin_max_weight, bin_name))
                    while bin_number[i]:
                        self.bin_list_with_n.append((bin_width, bin_length, bin_height, bin_max_weight, bin_name))
                        bin_number[i] -= 1
                    break

        material_list = []
        item_list = []
        item_count = 0
        item_data = json_data['tableData']
        baffle_extra = json_data['config']['baffle_extra']
        baffle_thickness = json_data['config']['baffle_thickness']
        self.baffle_thickness = baffle_thickness
        tray_height = 20 if json_data['config']['tray'] == "木架" else 15
        rule_vertical_wall = json_data['config']['rule_vertical_wall']
        overlap_way = json_data['config']['overlap_way']
        overlap_width = json_data['config']['overlap_width']
        for item in item_data:
            tray_number_in_whole_tray = 0
            d = math.sqrt(tubeApproximate+4*item['real_height']*(item['real_thickness']+0.7)/3.14)
            width = math.ceil(d / 10 + baffle_extra)  # 挡板面
            length = math.ceil((float(item['width']))/10 + 10)  # 无挡板面
            number = item['number']
            item_count += number
            if overlap_way == '1托3卷/6卷/托':
                tray_number_in_whole_tray = 1
                if width * 3 + tray_height <= bin_min_height:
                    height = width * 3 + tray_height
                    n = 3
                elif width * 2 + tray_height <= bin_min_height:
                    height = width * 2 + tray_height
                    n = 2
                else:
                    height = width + tray_height
                    n = 1
                json_data0 = {
                    "name": json_data['config']['tray'],
                    "size": f"{math.ceil(width)}*{math.ceil(length)}",
                    'unit': "只",
                    "number": math.ceil(number / n),
                    "date": arrive_date[0:10]
                }
                list_add_item(material_list, json_data0)
            elif overlap_way == '悬空2+1/悬空4+2':
                if width * 3 + tray_height * 2 <= bin_min_height:
                    height = width * 3 + tray_height * 2
                    n = 3
                    tray_number_in_whole_tray = 2
                elif width * 2 + tray_height <= bin_min_height:
                    height = width * 2 + tray_height
                    n = 2
                    tray_number_in_whole_tray = 1
                else:
                    height = width + tray_height
                    n = 1
                    tray_number_in_whole_tray = 1
                json_data0 = {
                    "name": json_data['config']['tray'],
                    "size": f"{math.ceil(width)}*{math.ceil(length)}",
                    'unit': "只",
                    "number": int((number+0.5) / 1.5) if n == 3 else number / n,
                    "date": arrive_date[0:10]
                }
                list_add_item(material_list, json_data0)
            else:
                if width * 2 + tray_height * 2 <= bin_min_height:
                    height = width * 2 + tray_height * 2
                    n = 2
                    tray_number_in_whole_tray = 2
                else:
                    height = width + tray_height
                    tray_number_in_whole_tray = 1
                    n = 1
                json_data0 = {
                    "name": json_data['config']['tray'],
                    "size": f"{math.ceil(width)}*{math.ceil(length)}",
                    'unit': "只",
                    "number": int(number),
                    "date": arrive_date[0:10]
                }
                list_add_item(material_list, json_data0)
            json_data0 = {
                "name": '挡板',
                "size": f"{math.ceil(width)}*{math.ceil(width)}*{baffle_thickness}",
                'unit': "张",
                "number": int(number * 2),
                "date": arrive_date[0:10]
            }
            list_add_item(material_list, json_data0)
            single_width = width
            if item['width'] <= overlap_width:
                n *= 2
                width *= 2
                # tray_number_in_whole_tray *= 2
            item_n_count = number / n
            # 添加完整的货物
            # item_list是整托货物的属性:宽 长 (高 partno 名字 托盘数量 挡板数量 忘了啥 挡板宽度)
            while item_n_count >= 1:
                item_list.append((width, length,
                                  (height, f"{item['order_thickness']}*{item['width']}*{item['order_height']}*{n}",
                                   f"{item['name']}", tray_number_in_whole_tray, 2 * n, round(d, 2), single_width)))
                item_n_count -= 1
            # 添加不完整的货物
            if number % n != 0:
                if number % n == 1:
                    item_list.append((single_width, length,
                                      (single_width+tray_height, f"{item['order_thickness']}*{item['width']}*{item['order_height']}*1",
                                       f"{item['name']}", 1, 2, round(d, 2), single_width)))
                elif number % n == 2:
                    if overlap_way == '1托3卷/6卷/托' or overlap_way == '悬空2+1/悬空4+2':
                        item_list.append((single_width, length, (single_width * 2 + tray_height,
                                          f"{item['order_thickness']}*{item['width']}*{item['order_height']}*2", f"{item['name']}", 1, 4, round(d, 2), single_width)))
                    else:
                        item_list.append((single_width, length, (single_width * 2 + tray_height,
                                                                 f"{item['order_thickness']}*{item['width']}*{item['order_height']}*2",
                                                                 f"{item['name']}", 2, 4, round(d, 2), single_width)))
                elif number % n == 3:
                    if overlap_way == '1托3卷/6卷/托':
                        item_list.append((single_width, length, (height,
                                          f"{item['order_thickness']}*{item['width']}*{item['order_height']}*3", f"{item['name']}", 1, 6, round(d, 2), single_width)))
                    elif overlap_way == '悬空2+1/悬空4+2':
                        item_list.append((single_width, length, (height,
                                          f"{item['order_thickness']}*{item['width']}*{item['order_height']}*3", f"{item['name']}", 2, 6, round(d, 2), single_width)))
                    else:
                        item_list.append((single_width, length, (height,
                                          f"{item['order_thickness']}*{item['width']}*{item['order_height']}*2", f"{item['name']}", 1, 4, round(d, 2), single_width)))
                        item_list.append((single_width,length,  (single_width+tray_height,
                                          f"{item['order_thickness']}*{item['width']}*{item['order_height']}*1", f"{item['name']}", 1, 2, round(d, 2), single_width)))
                elif number % n == 4:
                    item_list.append((width, length, (single_width * 2 + tray_height,
                                      f"{item['order_thickness']}*{item['width']}*{item['order_height']}*4", f"{item['name']}", 2, 8, round(d, 2), single_width)))
                else:
                    if overlap_way == '1托3卷/6卷/托':
                        item_list.append((single_width, length, (height,
                                          f"{item['order_thickness']}*{item['width']}*{item['order_height']}*3", f"{item['name']}", 1, 6, round(d, 2), single_width)))
                        item_list.append((single_width, length, (single_width*2 + tray_height,
                                          f"{item['order_thickness']}*{item['width']}*{item['order_height']}*2", f"{item['name']}", 1, 4, round(d, 2), single_width)))
                    else:
                        item_list.append((single_width, length, (height,
                                                                 f"{item['order_thickness']}*{item['width']}*{item['order_height']}*3",
                                                                 f"{item['name']}", 2, 6, round(d, 2), single_width)))
                        item_list.append((single_width, length, (single_width * 2 + tray_height,
                                                                 f"{item['order_thickness']}*{item['width']}*{item['order_height']}*2",
                                                                 f"{item['name']}", 1, 4, round(d, 2), single_width)))
        material_list = sorted(material_list, key=lambda x: x['name'])
        self.material_list = material_list
        self.item_list = item_list
        self.item_count = item_count
        self.task_id = task_id
        self.order_id = json_data['config']['orderId']
        self.rule_vertical_wall = rule_vertical_wall
        self.unpack_items = []
        self.unpack_items_count = 0
        # self.packer = newPacker(pack_algo=MaxRectsBlsf)

    def pack(self, algo=MaxRectsBlsf):

        # 设置字体（SimHei 是一个常用的支持中文的字体，可以替换为你系统中的其他字体）
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # 创建原料excel(包括未装入)
        # save_path = create_material_excel(self.material_list, self.task_id, self.order_id, self.arrive_date)

        result = {}

        packer = newPacker(pack_algo=algo)
        if algo == MaxRectsBssf:
            algo_name = 'MaxRectsBssf'
        elif algo == MaxRectsBaf:
            algo_name = 'MaxRectsBaf'
        elif algo == MaxRectsBlsf:
            algo_name = 'MaxRectsBlsf'
        elif algo == MaxRectsBbef:
            algo_name = 'MaxRectsBbef'
        else:
            algo_name = 'MaxRectsBiof'
        # 添加矩形到打包器
        for r in self.item_list:
            packer.add_rect(*r)

        # 添加容器
        for b in self.bin_list:
            packer.add_bin(*b)

        # 开始打包
        packer.pack(self.rule_vertical_wall)
        print(f"膜卷总数量{self.item_count}")

        # 清除耗材清单(为了后续统计仅装入的)
        self.material_list = []

        has_enclosed_hole = False
        enclosed_hole_area = 0

        # 每个容器
        for i, b in enumerate(self.bin_list_with_n):
            bin_width, bin_length, bin_height, bin_max_weight, bin_name = b
            # 创建一个图形
            fig, ax = plt.subplots(figsize=(bin_width/40, bin_length/40))
            bin_data = {'bin_width': bin_width, 'bin_length': bin_length, 'bin_height': bin_height,
                        'bin_max_weight': bin_max_weight, 'bin_name': bin_name}
            bin_result = []

            # 绘制箱子的边框
            ax.add_patch(Rectangle((0, 0), bin_width, bin_length, edgecolor='black', fill=None, lw=2))
            ax.text(bin_width / 2, bin_length + 5, f'车尾', ha='center')
            ax.text(bin_width / 2, -20, f'车头', ha='center')
            # 设置x轴和y轴范围，确保图像能包含所有箱子
            ax.set_xlim(0, bin_width)
            ax.set_ylim(0, bin_length)

            # 箱子内的矩形
            for j, rect in enumerate(packer.rect_list()):
                bin_idx, x, y, w, h, rid, rotation = rect
                if bin_idx == i:  # 确保矩形在当前的箱子里
                    bin_result.append({"position_x": x, "position_y": y, "length": w, "width": h, "height": rid[0],
                                       "name": f"{rid[1]}", "rotation": rotation, "id": j+1, "show_name1": f"高{round(rid[0], 1)}", "show_name2": f"卷膜信息{rid[1]}",
                                       "color": color_gradient((1-rid[0]/bin_height)*2) if rid[0]/bin_height > 0.5 else "#FFFF00",
                                       "tray_size": f"{math.ceil(w)}*{math.ceil(h)}" if rotation else f"{math.ceil(h)}*{math.ceil(w)}",
                                       "tray_number": rid[3],
                                       # "baffle_size": f"{math.ceil(h)}*{math.ceil(h)}*{self.baffle_thickness}" if rotation else f"{math.ceil(w)}*{math.ceil(w)}*{self.baffle_thickness}",
                                       "baffle_size": f"{math.ceil(rid[6])}*{math.ceil(rid[6])}*{self.baffle_thickness}",
                                       "baffle_number": rid[4], "d": rid[5]})
                    ax.add_patch(
                        Rectangle((x, y), w, h, edgecolor='black',
                                  facecolor=(1, (1-rid[0]/bin_height)*2 if rid[0]/bin_height > 0.5 else 1, 0),
                                  fill=True))
                    ax.text(x + w / 2, y + h / 2,
                            "\n".join(textwrap.wrap(f'{j+1} {rid[2]} {rid[1]} 侧' if rotation else f'{j+1} {rid[2]} {rid[1]} 正',
                                                    width=math.floor(w / 8))),
                            color='black', ha='center', va='center', fontsize=16, wrap=True)
                    # 统计所用耗材(仅限装入) 这里的逻辑是获取翻转前的 宽度 对照挡板宽度
                    if rotation:
                        now_v = h
                    else:
                        now_v = w
                    if abs(now_v-rid[6]) < 0.001:
                        show_w = math.ceil(rid[6])
                    else:
                        show_w = math.ceil(rid[6])*2
                    json_data0 = {
                        "name": self.tray_kind,
                        "size": f"{math.ceil(w)}*{show_w}" if rotation else f"{math.ceil(h)}*{show_w}",
                        # "size": f"{show_w}*{math.ceil(w)}",
                        'unit': "只",
                        "number": rid[3],
                        "date": self.arrive_date[0:10]
                    }
                    list_add_item(self.material_list, json_data0)
                    json_data0 = {
                        "name": '挡板',
                        # "size": f"{math.ceil(h)}*{math.ceil(h)}*{self.baffle_thickness}" if rotation
                        # else f"{math.ceil(w)}*{math.ceil(w)}*{self.baffle_thickness}",
                        "size": f"{math.ceil(rid[6])}*{math.ceil(rid[6])}*{self.baffle_thickness}",
                        'unit': "张",
                        "number": rid[4],
                        "date": self.arrive_date[0:10]
                    }
                    list_add_item(self.material_list, json_data0)
            # save_dir = os.path.join(os.path.dirname(__file__), 'static', 'images', self.task_id, f'{algo_name}_bin{i+1}.png')
            save_dir = os.path.join(get_static_images_dir(), self.task_id)
            plt.tight_layout()
            # 创建目录（如果不存在）
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            save_dir = os.path.join(save_dir, f'{algo_name}_bin{i+1}.png')
            fig.savefig(save_dir)
            print(f'图像已保存到: {save_dir}')
            save_dir = build_asset_path('images', self.task_id, f'{algo_name}_bin{i + 1}.png')
            layout_check = analyze_enclosed_holes(bin_width, bin_length, bin_result)
            has_enclosed_hole = has_enclosed_hole or layout_check["has_enclosed_hole"]
            enclosed_hole_area += layout_check["enclosed_hole_area"]
            result[f'bin{i}'] = {
                'container': bin_data,
                'placed_items': bin_result,
                'picture_address': save_dir,
                'layout_check': layout_check
            }
        self.material_list = sorted(self.material_list, key=lambda x: x['name'])
        save_path = create_material_excel(self.material_list, self.task_id, self.order_id, self.arrive_date, algo_name)
        result['excel_address'] = save_path
        result['excel_data'] = self.material_list
        unpack_item_info = ""
        for item in packer._unpack_item:
            unpack_item_info += f"{item}\n"
        result['remain_items'] = unpack_item_info
        result['remain_items_count'] = packer._unpack_item_count
        result['all_number'] = self.item_count
        result['has_enclosed_hole'] = has_enclosed_hole
        result['enclosed_hole_area'] = round(enclosed_hole_area, 2)
        result['algo_name'] = algo_name
        return result


# if __name__ == '__main__':
#     # 输入的矩形和容器
#     rectangles = [(78, 74, 1), (78, 74, 1), (84, 74, 1), (84, 74, 1), (86, 74, 1), (86, 74, 1), (87, 74, 1), (87, 74, 1),
#                   (102, 74, 1), (102, 74, 1), (78, 79, 2), (78, 79, 2), (82, 79, 2), (82, 79, 2), (86, 79, 2),
#                   (86, 79, 2), (87, 79, 2), (87, 79, 2), (94, 79, 2), (94, 79, 2), (102, 79, 2), (102, 79, 2), (154, 79, 2)]
#     bins = [(250, 800, 2)]
#
#     # 初始化打包器
#     packer = newPacker(pack_algo=MaxRectsBlsf)
#
#     # 添加矩形到打包器
#     for r in rectangles:
#         packer.add_rect(*r)
#
#     # 添加容器
#     for b in bins:
#         packer.add_bin(*b)
#
#     # 开始打包
#     packer.pack()
#
#     # 创建一个图形
#     fig, ax = plt.subplots()
#
#     # 定义不同颜色用于区分矩形
#     colors = ['red', 'green', 'blue', 'purple', 'orange']
#
#     # 绘制每个容器
#     bin_offset = 0  # 用于每个箱子的偏移，确保箱子不会相互重叠
#     for i, b in enumerate(bins):
#         bin_width, bin_height = b
#
#         # 绘制箱子的边框
#         ax.add_patch(Rectangle((bin_offset, 0), bin_width, bin_height, edgecolor='black', fill=None, lw=2))
#         ax.text(bin_offset + bin_width / 2, bin_height + 5, f'Bin {i+1}', ha='center')
#
#         # 绘制箱子内的矩形
#         for rect in packer.rect_list():
#             bin_idx, x, y, w, h, rid, rotation = rect
#             if bin_idx == i:  # 确保矩形在当前绘制的箱子里
#                 ax.add_patch(Rectangle((x + bin_offset, y), w, h, edgecolor='black', facecolor=colors[rid % len(colors)], fill=True))
#                 ax.text(x + w / 2 + bin_offset, y + h / 2, f'{rotation}', color='white', ha='center', va='center')
#
#         # 为下一个箱子添加水平偏移
#         bin_offset += bin_width + 50  # 50为两个箱子之间的间距
#
#     # 设置x轴和y轴范围，确保图像能包含所有箱子
#     ax.set_xlim(0, bin_offset)
#     ax.set_ylim(0, max(b[1] for b in bins))
#
#     # 显示图像
#     plt.gca().set_aspect('equal', adjustable='box')
#     plt.show()
