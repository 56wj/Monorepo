import math
from sko.GA import GA
from constants import RotationType, Axis
from auxiliary_methods import intersect, set2Decimal
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle, Circle
import matplotlib.gridspec as gridspec
# import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
import copy
import pandas as pd
import time
from Different_specifications import DifferentSpecifications
import os
import json
import warnings
import openpyxl
import shutil
from typing import List, Tuple, Optional
from functools import partial
from collections import defaultdict
from path_utils import get_static_images_dir, build_asset_path
from overlap_rules import can_stack_layer, parse_overlap_limits_cm

DEFAULT_NUMBER_OF_DECIMALS = 0
START_POSITION = [0, 0, 0]
path_count = 0
LOADING_RULE = 0  # 装载规则，1是平均装载，否则高度
patch_zu = ()
label_zu = ()
same_box = False
now_box = ''
new_bin = True


def return_height(item):
    return item.height


def return_level(item):
    return item.level


def return_number(item):
    return len(item.pack_tray)


def return_height0(item):
    if not item.is_mixed:
        return item.height
    else:
        return 0


def return_rate_of_height(item, height):
    if item.height > height:
        return item.height/(2*height)
    else:
        return item.height/height


def sum_height(item_list):
    height_count = 0
    for item in item_list:
        height_count+=item.height
    return height_count


def sum_weight(item_list):
    weight_count = 0
    for item in item_list:
        weight_count+=item.weight
    return weight_count


def all_zero_in(list):
    for i in list:
        if i != 0:
            return False
    return True


def list2name(tray_list):
    partno = ''
    for i in range(len(tray_list)):
        if i:
            partno += '+'
        partno += tray_list[i].partno
    return partno


# 把整托中的混装小托放在最后
def list_sort(tray_list):
    flag = False
    for i in range(len(tray_list)):
        if tray_list[i].is_mixed:
            flag = True
            break
    if flag:
        tray_list.append(tray_list.pop(i))
    return tray_list


def same_r_number_in_list(r_list, n_list, r):
    count = 0
    for i in range(len(r_list)):
        if abs(r_list[i] - r) < 0.0001:
            count += n_list[i]
    return count


def n_list_reduce_by_r(r_list, n_list, r, n):
    for i in range(len(r_list)):
        if abs(r_list[i] - r) < 0.001:
            if n_list[i] < n:
                n -= n_list[i]
                n_list[i] = 0
            else:
                n_list[i] -= n
                n = 0


def pack_all_items():
    return 0


def get_score(tray, target_height, way):
    score = 0
    if way == "balance":
        score = -(tray.height - target_height) ** 2
    else:
        if tray.height > target_height:
            score = -(tray.height - target_height) * 100000
        else:
            score = -(tray.height - target_height) ** 2
    return score


def best_exchange_in(tray1, tray2, target_height1, target_height2, way):
    if tray1.pack_tray[-1].is_mixed:
        tray1_usable_length = len(tray1.pack_tray) - 1
    else:
        tray1_usable_length = len(tray1.pack_tray)
    if tray2.pack_tray[-1].is_mixed:
        tray2_usable_length = len(tray2.pack_tray) - 1
    else:
        tray2_usable_length = len(tray2.pack_tray)
    best_programme = [0, 0]
    best_tray1 = copy.deepcopy(tray1)
    best_tray2 = copy.deepcopy(tray2)
    original_height_list1 = []
    original_height_list2 = []
    original_height1 = tray1.height
    original_height2 = tray2.height
    max_score = get_score(tray1, target_height1, way) + get_score(tray2, target_height2, way)
    # original_height_list1记录tray1发生交换前装的小托高度
    for i in range(len(tray1.pack_tray)):
        original_height_list1.append(tray1.pack_tray[i].height)
    for i in range(len(tray2.pack_tray)):
        original_height_list2.append(tray2.pack_tray[i].height)
    # 枚举所有交换子集的可能
    for i in range(pow(2, tray1_usable_length)):
        for j in range(pow(2, tray2_usable_length)):
            tray1_height_list = copy.deepcopy(original_height_list1)
            tray2_height_list = copy.deepcopy(original_height_list2)
            idx1 = num2idx_list(i)
            idx2 = num2idx_list(j)
            for k in idx1:
                tray2_height_list.append(tray1_height_list.pop(k))
            for k in idx2:
                tray1_height_list.append(tray2_height_list.pop(k))
            tray1.height = sum_list(tray1_height_list)
            tray2.height = sum_list(tray2_height_list)
            score = get_score(tray1, target_height1, way) + get_score(tray2, target_height2, way)
            if score > max_score:
                max_score = score
                best_programme = [i, j]
                best_tray1 = copy.deepcopy(tray1)
                best_tray2 = copy.deepcopy(tray2)
    tray1.height = original_height1
    tray2.height = original_height2
    return best_tray1, best_tray2, best_programme


def sum_list(num_list):
    count = 0
    for i in num_list:
        count += i
    return count


def num2idx_list(num):
    count = 0
    idx_list = []
    while num:
        if num % 2 == 1:
            idx_list.append(count)
        count += 1
        num = num // 2
    idx_list.reverse()
    return idx_list


def item_list2name(item_list):
    if len(item_list) == 0:
        return ""
    result = ""
    name = item_list[0].partno
    count = 0
    for item in item_list:
        if item.partno == name:
            count += 1
        else:
            if len(result) != 0:
                result += f"+{name}*{count}"
            else:
                result += f"{name}*{count}"
            count = 1
            name = item.partno
    if len(result) != 0:
        result += f"+{name}*{count}"
    else:
        result += f"{name}*{count}"
    return result


def list_exchange_by_programme(item_list, programme):
    item1 = item_list[programme[0]]
    item2 = item_list[programme[1]]
    exchange(item1, item2, programme[2:])
    if programme[2] or programme[3]:
        return True
    else:
        return False


def exchange(item1, item2, programme):
    tray1_exchange = num2idx_list(programme[0])
    tray2_exchange = num2idx_list(programme[1])
    for i in tray1_exchange:
        # if item1.pack_tray[i].height == 0:
        #     item1.pack_tray.pop(i)
        # else:
        item2.pack_tray.append(item1.pack_tray.pop(i))
    for i in tray2_exchange:
        # if item2.pack_tray[i].height == 0:
        #     item2.pack_tray.pop(i)
        # else:
        item1.pack_tray.append(item2.pack_tray.pop(i))
    item1.update_by_pack()
    item2.update_by_pack()
    return 0


def change_partno(partno, index):
    if partno.find('(') != -1 and partno.find(')') != -1:
        overlap_number = int(partno[partno.find('(') + 2:partno.find(')')])
        number = int(partno[index + 1:partno.find('(')])
        final_number = number * overlap_number
        return partno[:index + 1] + str(final_number)
    else:
        return partno


def create_and_save_plot(tray, name, title):
    global path_count
    save_path = get_static_images_dir()
    try:
        fig, ax = plt.subplots()
        max_length = 0
        max_width = 0
        for item in tray.items:
            r = item.length / 2
            circle = Circle((item.position[0] + r, item.position[1] + r), r, color=item.color, alpha=0.5)
            ax.add_patch(circle)
            if item.length + item.position[0] > max_length:
                max_length = item.length + item.position[0]
            if item.width + item.position[1] > max_width:
                max_width = item.width + item.position[1]
        ax.set_xlim(0, tray.real_length)
        ax.set_ylim(0, tray.real_width)
        plt.xlabel(f'长{tray.real_length},实际占用{round(max_length, 1)}')
        plt.plot([0, max_length], [max_width, max_width], color='red', linewidth=2)
        plt.ylabel(f'宽{tray.real_width},实际占用{round(max_width, 1)}')
        plt.plot([max_length, max_length], [0, max_width], color='red', linewidth=2)
        plt.title(title)
        path = os.path.join(save_path, str(name), f'{path_count}_{tray.items[0].name}.png')
        relative_path = build_asset_path('images', name, f'{path_count}_{tray.items[0].name}.png')
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        path_count += 1
        plt.savefig(path)
        # print(path)
        plt.close()
        return relative_path
    except Exception as e:
        # 记录错误信息
        with open('error_log.txt', 'a') as f:
            f.write(f"An error occurred in create_and_save_plot: {str(e)}\n")
        return None


def generator_excel(json_data, source_path, target_path, OrderId, tray_size):
    base = "货柜"
    content_base_idx = 6
    # 复制源文件
    if not os.path.exists(source_path):
        print(f"源文件不存在: {source_path}")
    else:
        try:
            shutil.copy(source_path, target_path)
        except Exception as e:
            print(f"复制文件时发生错误: {e}")

    try:
        # 打开目标文件
        workbook = openpyxl.load_workbook(target_path)

        # 工作表复制和重命名的逻辑
        idx = 0
        for _, item in enumerate(json_data):
            if "bin_item" in item:
                idx += 1
                num_tray = json_data[item]["whole_tray_number"]
                if str(num_tray) in workbook.sheetnames:
                    source_sheet = workbook[str(num_tray)]
                    # 使用copy_worksheet方法复制工作表
                    target_sheet = workbook.copy_worksheet(source_sheet)
                    target_sheet.title = base + str(idx)
                else:
                    print("没有此规格的模板")

        # 修改数值
        idx = 0
        for _, item in enumerate(json_data):
            if "bin_item" in item:
                idx += 1
                sheet = workbook[base + str(idx)]
                sheet['B3'] = OrderId
                sheet['G4'] = tray_size
                sheet['B4'] = idx

                excel_data = json_data[item]["excel_data"]
                for line, row in enumerate(excel_data):
                    row_data = excel_data[row]
                    row_idx = content_base_idx + line
                    sheet[f'A{row_idx}'] = row_data["no"]
                    sheet[f'B{row_idx}'] = row_data["thickness"]
                    sheet[f'C{row_idx}'] = row_data["width"]
                    sheet[f'D{row_idx}'] = row_data["number"]

        # 删除不需要的工作表
        for sheet_name in workbook.sheetnames:
            if base not in sheet_name:
                del workbook[sheet_name]

        # 保存更改
        workbook.save(target_path)

    except Exception as e:
        print(f"在操作 Excel 时发生错误：{e}")


# 定义圆形货物类
class MyCircle:
    def __init__(self, radius: float, id: int, partno: str = "", weight: float = 0.0, cylinder_length: float = 0):
        self.radius = radius
        self.id = id  # 用于标注
        self.partno = partno
        self.x: Optional[float] = None
        self.y: Optional[float] = None
        self.layer = 0
        self.weight = weight
        self.cylinder_length: float = cylinder_length

    def set_position(self, x: float, y: float):
        self.x = x
        self.y = y

    def is_position_set(self) -> bool:
        return self.x is not None and self.y is not None

class Bin2d:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.placed_circles: List[MyCircle] = []

    def check_overlap(self, new_circle: MyCircle) -> bool:
        for placed in self.placed_circles:
            distance = math.hypot(new_circle.x - placed.x, new_circle.y - placed.y)
            if distance < (new_circle.radius + placed.radius - 0.001):
                return True
        return False

    def is_within_bin(self, circle: MyCircle) -> bool:
        return (circle.x - circle.radius >= 0 and
                circle.x + circle.radius <= self.width and
                circle.y - circle.radius >= 0 and
                circle.y + circle.radius <= self.height)

    def place_circle_tangent_to_one_and_ground(self, new_circle: MyCircle, placed_circle: MyCircle) -> List[
        Tuple[float, float]]:
        """
        尝试将新圆形货物放置在与一个已放置圆形货物和地面相切的位置
        """
        r_new = new_circle.radius
        r_placed = placed_circle.radius
        x_placed = placed_circle.x
        y_placed = placed_circle.y

        # 新圆形货物的y坐标固定为半径（与地面相切）
        y_new = r_new

        # 计算新圆形货物的x坐标，使其与已放置圆形货物相切
        try:
            dx = math.sqrt((r_new + r_placed) ** 2 - (y_new - y_placed) ** 2)
        except ValueError:
            # 无法相切
            return []

        positions = [
            (x_placed - dx, y_new),
            (x_placed + dx, y_new)
        ]
        return positions

    def place_circle_tangent_to_two_circles(self, new_circle: MyCircle, circle1: MyCircle, circle2: MyCircle) -> List[
        Tuple[float, float]]:
        """
        尝试将新圆形货物放置在与两个已放置圆形货物相切的位置
        """
        r_new = new_circle.radius
        x1, y1, r1 = circle1.x, circle1.y, circle1.radius
        x2, y2, r2 = circle2.x, circle2.y, circle2.radius

        # 计算两个支持圆的中心距离
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)

        # 新圆形货物与两个支持圆的距离
        d1 = r_new + r1
        d2 = r_new + r2

        # 检查是否存在交点
        if dist > (d1 + d2) or dist < abs(d1 - d2):
            return []  # 无交点

        # 计算交点
        a = (d1 ** 2 - d2 ** 2 + dist ** 2) / (2 * dist)
        h_sq = d1 ** 2 - a ** 2
        if h_sq < 0:
            return []
        h = math.sqrt(h_sq)

        xm = x1 + a * dx / dist
        ym = y1 + a * dy / dist

        xs1 = xm + h * dy / dist
        ys1 = ym - h * dx / dist
        xs2 = xm - h * dy / dist
        ys2 = ym + h * dx / dist

        return [(xs1, ys1), (xs2, ys2)]

    def place_circle(self, new_circle: MyCircle, lying_limit: int = 4) -> bool:
        # 第一遍遍历：尝试与一个已放置圆和地面相切
        for placed in self.placed_circles:
            possible_positions = self.place_circle_tangent_to_one_and_ground(new_circle, placed)
            for x, y in possible_positions:
                new_circle.set_position(x, y)
                if self.is_within_bin(new_circle) and not self.check_overlap(new_circle):
                    new_circle.layer = 1
                    # self.placed_circles.append(new_circle)
                    return True
                else:
                    new_circle.set_position(None, None)  # 重置位置

        # 第二遍遍历：尝试与两个已放置圆相切
        n = len(self.placed_circles)
        for i in range(n):
            for j in range(i + 1, n):
                circle1 = self.placed_circles[i]
                circle2 = self.placed_circles[j]
                possible_positions = self.place_circle_tangent_to_two_circles(new_circle, circle1, circle2)
                for x, y in possible_positions:
                    new_circle.set_position(x, y)
                    if self.is_within_bin(new_circle) and not self.check_overlap(new_circle) and ((circle1.x < x and x < circle2.x) or (circle2.x < x and x < circle1.x)) and min(circle1.layer, circle2.layer)+1 <= lying_limit:
                        new_circle.layer = min(circle1.layer, circle2.layer)+1
                        # self.placed_circles.append(new_circle)
                        return True
                    else:
                        new_circle.set_position(None, None)  # 重置位置

        # 如果无法放置
        return False


class Item:
    def __init__(self, partno, typeof, lwh, weight, level=1, pack_tray=[], color="red", updown=False,
                 pack_item=[], pack_item_number=[], overlap_layers=1, name='', is_mixed=False, is_overlap=False,
                 is_lying=False, address=''):
        self.partno = partno  # 转化后的名称
        self.name = name  # 品名
        self.typeof = typeof
        self.length = lwh[0]
        self.width = lwh[1]
        self.height = lwh[2]
        self.weight = weight
        # Packing Priority level ,choose 1-3
        self.level = level
        # Upside down? True or False
        self.updown = updown if typeof == 'cube' else False
        # Draw item color
        self.color = color
        self.rotation_type = 0
        self.position = START_POSITION
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
        self.is_mixed = is_mixed  # 是否是混装
        self.is_overlap = is_overlap  # 是否膜叠膜
        self.pack_item = pack_item  # 小托属性，记载装载的货物
        self.pack_item_number = pack_item_number  # 小托属性，记载装载的货物数量
        self.overlap_layers = overlap_layers  # 小托属性，记载膜叠膜的层数
        self.pack_tray = pack_tray  # 整托属性，记载装载小托,[]代表只有本身
        self.is_lying = is_lying
        self.address = address

    def formatNumbers(self, number_of_decimals):
        ''' '''
        self.width = set2Decimal(self.width, number_of_decimals)
        self.height = set2Decimal(self.height, number_of_decimals)
        self.length = set2Decimal(self.length, number_of_decimals)
        self.weight = set2Decimal(self.weight, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def string(self):
        ''' '''
        return "%s(%sx%sx%s, weight: %s) pos(%s) rt(%s) vol(%s)" % (
            self.partno, self.length, self.width, self.height, self.weight,
            self.position, self.rotation_type, self.getVolume()
        )

    def getVolume(self):
        return set2Decimal(self.width * self.height * self.length, self.number_of_decimals)

    def getMaxArea(self):
        a = sorted([self.length, self.width, self.height], reverse=True) if self.updown == True else [self.length,
                                                                                                      self.width,
                                                                                                      self.height]

        return set2Decimal(a[0] * a[1], self.number_of_decimals)

    def getDimension(self):
        if self.rotation_type == RotationType.RT_LWH:
            dimension = [self.length, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WLH:
            dimension = [self.width, self.length, self.height]
        elif self.rotation_type == RotationType.RT_WHL:
            dimension = [self.width, self.height, self.length]
        elif self.rotation_type == RotationType.RT_HWL:
            dimension = [self.height, self.width, self.length]
        elif self.rotation_type == RotationType.RT_HLW:
            dimension = [self.height, self.length, self.width]
        elif self.rotation_type == RotationType.RT_LHW:
            dimension = [self.length, self.height, self.width]
        else:
            dimension = []

        return dimension

    # 内部含有小托改变后，更新高度、重量、含有小托顺序(横放最后，混装其次)
    def update_by_pack(self):
        height_count = 0
        weight_count = 0
        for i in self.pack_tray:
            height_count += i.height
            weight_count += i.weight
        self.height = height_count
        self.weight = weight_count
        for i in range(len(self.pack_tray) - 1, -1, -1):
            if self.pack_tray[i].height == 0:
                self.pack_tray.pop(i)
        for i in range(len(self.pack_tray)):
            if self.pack_tray[i].is_mixed:
                self.pack_tray.append(self.pack_tray.pop(i))
                break
        for i in range(len(self.pack_tray)):
            if self.pack_tray[i].is_lying:
                self.pack_tray.append(self.pack_tray.pop(i))
                break
        return height_count


class Tray:
    def __init__(self, name, lwh, extra_length, extra_width, weight, color):
        self.name = name
        self.length = lwh[0] + extra_length
        self.width = lwh[1] + extra_width
        self.height = lwh[2]
        self.extra_length = extra_length
        self.extra_width = extra_width
        self.weight = weight
        self.color = color
        self.items = []
        self.position = [0, 0, 0]
        self.number = 0
        self.real_length = self.length
        self.real_width = self.width
        self.real_height = self.height

    def clear_tray(self):
        self.items = []
        return

    def reset_tray(self):
        tem = self.length
        self.length = self.real_length
        self.real_length = tem
        tem = self.width
        self.width = self.real_width
        self.real_width = tem
        tem = self.height
        self.height = self.real_height
        self.real_height = tem
        return


class Bin:
    def __init__(self, partno, lwh, max_weight=10000, corner=0, put_type=1, max_whole_number=20):
        self.partno = partno
        self.length = lwh[0]
        self.width = lwh[1]
        self.height = lwh[2]
        self.max_weight = max_weight
        self.corner = corner
        self.items = []
        self.fit_items = np.array([[0, lwh[0], 0, lwh[1], 0, 0]])
        self.unfitted_items = []
        self.trays = []
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
        self.fix_point = False
        self.check_stable = False
        self.support_surface_ratio = 0
        self.put_type = put_type
        # used to put gravity distribution
        self.gravity = []
        self.volume = 0
        self.patch_zu = ()
        self.label_zu = ()
        self.max_whole_number = max_whole_number
        self.item_number = 0

    def formatNumbers(self, number_of_decimals):
        self.length = set2Decimal(self.length, number_of_decimals)
        self.width = set2Decimal(self.width, number_of_decimals)
        self.height = set2Decimal(self.height, number_of_decimals)
        self.max_weight = set2Decimal(self.max_weight, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def string(self):
        return "%s(%sx%sx%s, max_weight:%s) vol(%s)" % (
            self.partno, self.length, self.width, self.height, self.max_weight,
            self.getVolume()
        )

    def getVolume(self):
        return set2Decimal(
            self.width * self.height * self.length, self.number_of_decimals
        )

    def getTotalWeight(self):
        total_weight = 0

        for item in self.items:
            total_weight += item.weight

        return total_weight

    def putItem(self, item, pivot, axis=None):
        ''' put item in bin '''
        fit = False
        valid_item_position = item.position
        item.position = pivot
        rotate = RotationType.ALL if item.updown == True else RotationType.Notupdown
        for i in range(0, len(rotate)):
            item.rotation_type = i
            dimension = item.getDimension()
            # rotatate
            if (
                    self.length < pivot[0] + dimension[0] or
                    self.width < pivot[1] + dimension[1] or
                    self.height < pivot[2] + dimension[2]
            ):
                continue

            fit = True

            for current_item_in_bin in self.items:
                if intersect(current_item_in_bin, item):
                    fit = False
                    break

            if fit:
                if self.getTotalWeight() + item.weight > self.max_weight:
                    fit = False
                    return fit

                # fix point float prob
                if 1:  # self.fix_point == True :

                    [l, w, h] = dimension
                    [x, y, z] = [float(pivot[0]), float(pivot[1]), float(pivot[2])]

                    for i in range(3):
                        x = self.checkLength([x, x + float(l), y, y + float(w), z, z + float(h)])
                        y = self.checkWidth([x, x + float(l), y, y + float(w), z, z + float(h)])
                        z = self.checkHeight([x, x + float(l), y, y + float(w), z, z + float(h)])

                    # check stability on item
                    # rule :
                    # 1. Define a support ratio, if the ratio below the support surface does not exceed this ratio, compare the second rule.
                    # 2. If there is no support under any vertices of the bottom of the item, then fit = False.
                    # if self.check_stable == True:
                    #     # Cal the surface area of item.
                    #     item_area_lower = int(dimension[0] * dimension[1])
                    #     # Cal the surface area of the underlying support.
                    #     support_area_upper = 0
                    #     for i in self.fit_items:
                    #         # Verify that the lower support surface area is greater than the upper support surface area * support_surface_ratio.
                    #         if z == i[5]:
                    #             area = len(set([j for j in range(int(x), int(x + int(w)))]) & set(
                    #                 [j for j in range(int(i[0]), int(i[1]))])) * \
                    #                    len(set([j for j in range(int(y), int(y + int(h)))]) & set(
                    #                        [j for j in range(int(i[2]), int(i[3]))]))
                    #             support_area_upper += area
                    #
                    #     # If not , get four vertices of the bottom of the item.
                    #     if support_area_upper / item_area_lower < self.support_surface_ratio:
                    #         four_vertices = [[x, y], [x + float(w), y], [x, y + float(h)], [x + float(w), y + float(h)]]
                    #         #  If any vertices is not supported, fit = False.
                    #         c = [False, False, False, False]
                    #         for i in self.fit_items:
                    #             if z == i[5]:
                    #                 for jdx, j in enumerate(four_vertices):
                    #                     if (i[0] <= j[0] <= i[1]) and (i[2] <= j[1] <= i[3]):
                    #                         c[jdx] = True
                    #         if False in c:
                    #             item.position = valid_item_position
                    #             fit = False
                    #             return fit

                    # self.fit_items = np.append(self.fit_items,
                    #                            np.array([[x, x + float(l), y, y + float(w), z, z + float(h)]]), axis=0)
                    # item.position = [set2Decimal(x), set2Decimal(y), set2Decimal(z)]

                if fit:
                    self.items.append(copy.deepcopy(item))

            else:
                item.position = valid_item_position

            return fit

        else:
            item.position = valid_item_position

        return fit

    def checkLength(self, unfix_point):
        ''' fix item position z '''
        z_ = [[0, 0], [float(self.length), float(self.length)]]
        for j in self.fit_items:
            # creat x set
            x_bottom = set([i for i in range(int(j[0]), int(j[1]))])
            x_top = set([i for i in range(int(unfix_point[0]), int(unfix_point[1]))])
            # creat y set
            y_bottom = set([i for i in range(int(j[2]), int(j[3]))])
            y_top = set([i for i in range(int(unfix_point[2]), int(unfix_point[3]))])
            # find intersection on x set and y set.
            if len(x_bottom & x_top) != 0 and len(y_bottom & y_top) != 0:
                z_.append([float(j[4]), float(j[5])])
        top_depth = unfix_point[5] - unfix_point[4]
        # find diff set on z_.
        z_ = sorted(z_, key=lambda z_: z_[1])
        for j in range(len(z_) - 1):
            if z_[j + 1][0] - z_[j][1] >= top_depth:
                return z_[j][1]
        return unfix_point[4]

    def checkWidth(self, unfix_point):
        ''' fix item position x '''
        x_ = [[0, 0], [float(self.width), float(self.width)]]
        for j in self.fit_items:
            # creat z set
            z_bottom = set([i for i in range(int(j[4]), int(j[5]))])
            z_top = set([i for i in range(int(unfix_point[4]), int(unfix_point[5]))])
            # creat y set
            y_bottom = set([i for i in range(int(j[2]), int(j[3]))])
            y_top = set([i for i in range(int(unfix_point[2]), int(unfix_point[3]))])
            # find intersection on z set and y set.
            if len(z_bottom & z_top) != 0 and len(y_bottom & y_top) != 0:
                x_.append([float(j[0]), float(j[1])])
        top_width = unfix_point[1] - unfix_point[0]
        # find diff set on x_bottom and x_top.
        x_ = sorted(x_, key=lambda x_: x_[1])
        for j in range(len(x_) - 1):
            if x_[j + 1][0] - x_[j][1] >= top_width:
                return x_[j][1]
        return unfix_point[0]

    def checkHeight(self, unfix_point):
        '''fix item position y '''
        y_ = [[0, 0], [float(self.height), float(self.height)]]
        for j in self.fit_items:
            # creat x set
            x_bottom = set([i for i in range(int(j[0]), int(j[1]))])
            x_top = set([i for i in range(int(unfix_point[0]), int(unfix_point[1]))])
            # creat z set
            z_bottom = set([i for i in range(int(j[4]), int(j[5]))])
            z_top = set([i for i in range(int(unfix_point[4]), int(unfix_point[5]))])
            # find intersection on x set and z set.
            if len(x_bottom & x_top) != 0 and len(z_bottom & z_top) != 0:
                y_.append([float(j[2]), float(j[3])])
        top_height = unfix_point[3] - unfix_point[2]
        # find diff set on y_bottom and y_top.
        y_ = sorted(y_, key=lambda y_: y_[1])
        for j in range(len(y_) - 1):
            if y_[j + 1][0] - y_[j][1] >= top_height:
                return y_[j][1]

        return unfix_point[2]

    def addCorner(self):
        '''add container coner '''
        if self.corner != 0:
            corner = set2Decimal(self.corner)
            corner_list = []
            for i in range(8):
                a = Item(
                    partno='corner{}'.format(i),
                    name='corner',
                    typeof='cube',
                    lwh=(corner, corner, corner),
                    weight=0,
                    level=0,
                    updown=True,
                    color='#000000')

                corner_list.append(a)
            return corner_list

    def putCorner(self, info, item):
        '''put coner in bin '''
        fit = False
        x = set2Decimal(self.length - self.corner)
        y = set2Decimal(self.width - self.corner)
        z = set2Decimal(self.height - self.corner)
        pos = [[0, 0, 0], [0, 0, z], [0, y, z], [0, y, 0], [x, y, 0], [x, 0, 0], [x, 0, z], [x, y, z]]
        item.position = pos[info]
        self.items.append(item)

        corner = [float(item.position[0]), float(item.position[0]) + float(self.corner), float(item.position[1]),
                  float(item.position[1]) + float(self.corner), float(item.position[2]),
                  float(item.position[2]) + float(self.corner)]

        self.fit_items = np.append(self.fit_items, np.array([corner]), axis=0)
        return

    def clearBin(self):
        ''' clear item which in bin '''
        self.items = []
        self.fit_items = np.array([[0, self.length, 0, self.width, 0, 0]])
        return


class Packer:

    def __init__(self):
        self.bins = []
        self.trays = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0
        self.binding = []
        self.max = []
        self.same_r_name = []
        self.same_r_list = []
        self.same_r_item = []
        self.same_r_number = []
        self.packed_items = []

    def sort_by_partno(self):  # 按r分大类，按分小类
        for item in self.items:
            in_list = False
            if not item.is_mixed:
                radius = item.pack_item[0].length / 2
            else:
                radius = 0
            for i in range(len(self.same_r_list)):
                if abs(self.same_r_list[i] - radius) < 0.0001:
                    in_item_list = False
                    for j in range(len(self.same_r_item[i])):
                        if self.same_r_item[i][j].partno == item.partno:
                            self.same_r_number[i][j] += 1
                            in_item_list = True
                            break
                    if not in_item_list:
                        self.same_r_item[i].append(item)
                        self.same_r_number[i].append(1)
                    in_list = True
                    break
            if not in_list:
                self.same_r_list.append(radius)
                self.same_r_item.append([])
                self.same_r_item[len(self.same_r_list) - 1].append(item)
                self.same_r_number.append([])
                self.same_r_number[len(self.same_r_list) - 1].append(1)
        return 0

    def pack_whole_tray(self):
        max_h = self.bins[0].depth
        pack_items = []
        all_h = 0
        for items in self.same_r_item:
            while items:
                all_h += items[0].depth
                items.pop(index=0)
                while items:
                    count = 0
                    if all_h + items[count] < max_h:
                        all_h += items[count]
                        items.pop[count]
                    else:
                        count += 1

    def addBin(self, bin):
        return self.bins.append(bin)

    def addItem(self, item):
        self.total_items = len(self.items) + 1
        return self.items.append(copy.deepcopy(item))

    def pack2Bin(self, bin, item, fix_point, check_stable, support_surface_ratio):
        ''' pack item to bin '''
        fitted = False
        bin.fix_point = fix_point
        bin.check_stable = check_stable
        bin.support_surface_ratio = support_surface_ratio

        # first put item on (0,0,0) , if corner exist ,first add corner in box. 
        if bin.corner != 0 and not bin.items:
            corner_lst = bin.addCorner()
            for i in range(len(corner_lst)):
                bin.putCorner(i, corner_lst[i])

        elif not bin.items:
            response = bin.putItem(item, item.position)
            bin.volume += item.width * item.height * item.length  # 统计总体积

            if not response:
                bin.unfitted_items.append(item)
            return

        for axis in range(0, 2):
            items_in_bin = bin.items
            for ib in items_in_bin:
                pivot = [0, 0, 0]
                l, w, h = ib.getDimension()
                if axis == Axis.Width:
                    pivot = [ib.position[0], ib.position[1] + w, ib.position[2]]
                elif axis == Axis.Height:
                    pivot = [ib.position[0], ib.position[1], ib.position[2] + h]
                elif axis == Axis.Length:
                    pivot = [ib.position[0] + l, ib.position[1], ib.position[2]]

                if bin.putItem(item, pivot, axis):
                    bin.volume += item.width * item.height * item.length  # 统计总体积
                    fitted = True
                    break
            if fitted:
                break
        if not fitted:
            bin.unfitted_items.append(item)

    def sortBinding(self, bin):
        ''' sorted by binding '''
        for i in self.items:
            print(i.name)
        b, front, back = [], [], []
        for i in range(len(self.binding)):
            b.append([])
            for item in self.items:
                if item.name in self.binding[i]:
                    b[i].append(item)
                elif item.name not in self.binding:
                    if len(b[0]) == 0 and item not in front:
                        front.append(item)
                    elif item not in back and item not in front:
                        back.append(item)

        min_c = min([len(i) for i in b])

        sort_bind = []
        for i in range(min_c):
            for j in range(len(b)):
                sort_bind.append(b[j][i])

        for i in b:
            for j in i:
                if j not in sort_bind:
                    self.unfit_items.append(j)

        self.items = front + sort_bind + back
        for i in self.items:
            print(i.name)
        return

    def putOrder(self):
        '''Arrange the order of items '''
        r = []
        for i in self.bins:
            # open top container
            if i.put_type == 2:
                i.items.sort(key=lambda item: item.position[0], reverse=False)
                i.items.sort(key=lambda item: item.position[1], reverse=False)
                i.items.sort(key=lambda item: item.position[2], reverse=False)
            # general container
            elif i.put_type == 1:
                i.items.sort(key=lambda item: item.position[1], reverse=False)
                i.items.sort(key=lambda item: item.position[2], reverse=False)
                i.items.sort(key=lambda item: item.position[0], reverse=False)
            else:
                pass
        return

    def gravityCenter(self, bin):
        ''' 
        Deviation Of Cargo gravity distribution
        '''
        w = int(bin.width)
        h = int(bin.height)
        d = int(bin.depth)

        area1 = [set(range(0, w // 2 + 1)), set(range(0, h // 2 + 1)), 0]
        area2 = [set(range(w // 2 + 1, w + 1)), set(range(0, h // 2 + 1)), 0]
        area3 = [set(range(0, w // 2 + 1)), set(range(h // 2 + 1, h + 1)), 0]
        area4 = [set(range(w // 2 + 1, w + 1)), set(range(h // 2 + 1, h + 1)), 0]
        area = [area1, area2, area3, area4]

        for i in bin.items:

            x_st = int(i.position[0])
            y_st = int(i.position[1])
            if i.rotation_type == 0:
                x_ed = int(i.position[0] + i.width)
                y_ed = int(i.position[1] + i.height)
            elif i.rotation_type == 1:
                x_ed = int(i.position[0] + i.height)
                y_ed = int(i.position[1] + i.width)
            elif i.rotation_type == 2:
                x_ed = int(i.position[0] + i.height)
                y_ed = int(i.position[1] + i.depth)
            elif i.rotation_type == 3:
                x_ed = int(i.position[0] + i.depth)
                y_ed = int(i.position[1] + i.height)
            elif i.rotation_type == 4:
                x_ed = int(i.position[0] + i.depth)
                y_ed = int(i.position[1] + i.width)
            elif i.rotation_type == 5:
                x_ed = int(i.position[0] + i.width)
                y_ed = int(i.position[1] + i.depth)

            x_set = set(range(x_st, int(x_ed) + 1))
            y_set = set(range(y_st, y_ed + 1))

            # cal gravity distribution
            for j in range(len(area)):
                if x_set.issubset(area[j][0]) and y_set.issubset(area[j][1]):
                    area[j][2] += int(i.weight)
                    break
                # include x and !include y
                elif x_set.issubset(area[j][0]) == True and y_set.issubset(area[j][1]) == False and len(
                        y_set & area[j][1]) != 0:
                    y = len(y_set & area[j][1]) / (y_ed - y_st) * int(i.weight)
                    area[j][2] += y
                    if j >= 2:
                        area[j - 2][2] += (int(i.weight) - x)
                    else:
                        area[j + 2][2] += (int(i.weight) - y)
                    break
                # include y and !include x
                elif x_set.issubset(area[j][0]) == False and y_set.issubset(area[j][1]) == True and len(
                        x_set & area[j][0]) != 0:
                    x = len(x_set & area[j][0]) / (x_ed - x_st) * int(i.weight)
                    area[j][2] += x
                    if j >= 2:
                        area[j - 2][2] += (int(i.weight) - x)
                    else:
                        area[j + 2][2] += (int(i.weight) - x)
                    break
                # !include x and !include y
                elif x_set.issubset(area[j][0]) == False and y_set.issubset(area[j][1]) == False and len(
                        y_set & area[j][1]) != 0 and len(x_set & area[j][0]) != 0:
                    all = (y_ed - y_st) * (x_ed - x_st)
                    y = len(y_set & area[0][1])
                    y_2 = y_ed - y_st - y
                    x = len(x_set & area[0][0])
                    x_2 = x_ed - x_st - x
                    area[0][2] += x * y / all * int(i.weight)
                    area[1][2] += x_2 * y / all * int(i.weight)
                    area[2][2] += x * y_2 / all * int(i.weight)
                    area[3][2] += x_2 * y_2 / all * int(i.weight)
                    break

        r = [area[0][2], area[1][2], area[2][2], area[3][2]]
        result = []
        for i in r:
            result.append(round(i / sum(r) * 100, 2))
        return result

    def pack_cylinder(self):
        max_number = 0  # 记录最多摆放个数
        count = 0  # 记录摆放个数
        max_way = 0  # 记录摆放方式 0 代表横放 1 代表竖放
        max_c_row = 0  # 最大摆放方式下普通摆放方式有几列
        max_s_row = 0
        r = self.items[0].width / 2
        box_w = self.trays[0].width
        box_h = self.trays[0].height
        # 横着放
        common_row = int(box_h / (2 * r))  # 一行摆多少个
        if common_row * 2 * r + r <= box_h:
            special_row = common_row
        else:
            special_row = common_row - 1
        max_row = int(box_w / (2 * r))
        for i in range(max_row):
            i = i + 1
            length = box_w - i * 2 * r
            special_row_number = int(length / (r * math.sqrt(3)))
            count = int(special_row_number / 2) * common_row + int(
                (special_row_number + 1) / 2) * special_row + i * common_row
            if count > max_number:
                max_number = count
                max_c_row = i
                max_s_row = special_row_number
        # 竖着放
        common_row = int(box_w / (2 * r))
        if common_row * 2 * r + r <= box_w:
            special_row = common_row
        else:
            special_row = common_row - 1
        max_row = int(box_h / (2 * r))
        for i in range(max_row):
            i = i + 1
            length = box_h - i * 2 * r
            special_row_number = int(length / (r * math.sqrt(3)))
            count = int(special_row_number / 2) * common_row + int(
                (special_row_number + 1) / 2) * special_row + i * common_row
            if count > max_number:
                max_number = count
                max_c_row = i
                max_s_row = special_row_number
                max_way = 1
        box_count = 0
        if max_way:
            start_h = 2 * r * (max_c_row - 1) + r * math.sqrt(3)
            for i in range(max_c_row):
                for j in range(common_row):
                    if box_count + 1 > len(self.items):
                        break
                    self.items[box_count].position = [j * 2 * r, i * 2 * r, 0]
                    self.trays[0].items.append(self.items[box_count])
                    box_count += 1
                if box_count + 1 > len(self.items):
                    break
            for i in range(max_s_row):
                if i % 2 == 0:
                    for j in range(special_row):
                        if box_count + 1 > len(self.items):
                            break
                        self.items[box_count].position = [j * 2 * r + r, i * math.sqrt(3) * r + start_h, 0]
                        self.trays[0].items.append(self.items[box_count])
                        box_count += 1
                else:
                    for j in range(common_row):
                        if box_count + 1 > len(self.items):
                            break
                        self.items[box_count].position = [j * 2 * r, i * math.sqrt(3) * r + start_h, 0]
                        self.trays[0].items.append(self.items[box_count])
                        box_count += 1
                if box_count + 1 > len(self.items):
                    break
        else:
            start_w = 2 * r * (max_c_row - 1) + r * math.sqrt(3)
            common_row = int(box_h / (2 * r))  # 一行摆多少个
            if common_row * 2 * r + r <= box_h:
                special_row = common_row
            else:
                special_row = common_row - 1
            for i in range(max_c_row):
                for j in range(common_row):
                    if box_count + 1 > len(self.items):
                        break
                    self.items[box_count].position = [i * 2 * r, j * 2 * r, 0]
                    self.trays[0].items.append(self.items[box_count])
                    # print(box_count, self.items[box_count].position)
                    box_count += 1
                if box_count + 1 > len(self.items):
                    break
            for i in range(max_s_row):
                if i % 2 == 0:
                    for j in range(special_row):
                        if box_count + 1 > len(self.items):
                            break
                        self.items[box_count].position = [i * math.sqrt(3) * r + start_w, j * 2 * r + r, 0]
                        self.trays[0].items.append(self.items[box_count])
                        box_count += 1
                else:
                    for j in range(common_row):
                        if box_count + 1 > len(self.items):
                            break
                        self.items[box_count].position = [i * math.sqrt(3) * r + start_w, j * 2 * r, 0]
                        self.trays[0].items.append(self.items[box_count])
                        box_count += 1
                if box_count + 1 > len(self.items):
                    break
        return max_number

    def pack_cylinder1(self):
        # print("正在尝试装载托盘", py3dbp.myexample.tray_count)
        # 半径
        r = self.items[0].width / 2
        # 箱体参数
        box_width = self.trays[0].width
        box_length = self.trays[0].height
        # fit阈值
        target_fitness = 0.1
        # GA参数
        size_pop = 1000
        max_iter = 20
        max_epochs = 20
        # 计算初始数量
        n_num = int((box_width / (r * 2))) * int((box_length / (r * 2)))

        def func(x):
            total = 0
            coordinate_x = x[:n_num]
            coordinate_y = x[n_num:]
            for i in range(n_num):
                if coordinate_x[i] - r < 0:
                    total -= coordinate_x[i] - r
                if coordinate_x[i] + r > box_length:
                    total += (coordinate_x[i] + r - box_length)
                if coordinate_y[i] - r < 0:
                    total -= coordinate_y[i] - r
                if coordinate_y[i] + r > box_width:
                    total += coordinate_y[i] + r - box_width
            for i in range(n_num):
                for j in range(i + 1, n_num):
                    if np.sqrt((coordinate_x[j] - coordinate_x[i]) ** 2 + (
                            coordinate_y[j] - coordinate_y[i]) ** 2) < r + r:
                        total += (r + r - np.sqrt(
                            (coordinate_x[j] - coordinate_x[i]) ** 2 + (coordinate_y[j] - coordinate_y[i]) ** 2)) * 2
            return total

        best_x, best_y = 0, 0
        while (True):
            print(f'放入数量为:{n_num}时')
            is_load = False
            lb = [0 + r] * n_num * 2
            ub = [box_length - r] * n_num + [box_width - r] * n_num
            ga = GA(func=func, n_dim=n_num * 2, size_pop=size_pop, max_iter=max_iter, lb=lb, ub=ub)
            for i in range(max_epochs):
                temp_x, temp_y = ga.run()

                # print(f'epoch:{i} , fit:{temp_y}')
                if temp_y <= target_fitness:
                    print(f"放入数量为{n_num},找到最佳结果：{temp_x}")
                    best_x, best_y = temp_x, temp_y
                    is_load = True
                    break

            if is_load:
                n_num += 1
            else:
                # print(f'放入数量为{n_num}，未找到结果')
                break
        n_num -= 1
        # print(f"放入数量为{n_num}")
        coordinate_x = best_x[:n_num]
        coordinate_y = best_x[n_num:]
        for i in range(n_num):
            self.items[i].position = [coordinate_x[i] - r, coordinate_y[i] - r, 0]
            self.trays[0].items.append(self.items[i])
        return n_num

    def pack_cylinder2(self):
        # 临时增加货物，防止
        for i in range(20):
            self.items.append(copy.deepcopy(self.items[0]))
        # 基本数据
        r = self.items[0].length / 2
        box_l = self.trays[0].length
        box_w = self.trays[0].width
        # 30 60 90 布局规整
        max_count = 0  # 记录最多摆放个数
        count = 0  # 记录摆放个数
        max_way = 0  # 记录摆放方式 0 代表横放 1 代表竖放
        max_c_row = 0  # 最大摆放方式下对正摆放方式有几列
        max_s_row = 0
        # 横着放
        common_row = int(box_w / (2 * r))  # 一行摆多少个
        if common_row * 2 * r + r <= box_w:
            special_row = common_row
        else:
            special_row = common_row - 1
        max_row = int(box_l / (2 * r))
        for i in range(max_row):
            i = i + 1
            length = box_l - i * 2 * r
            special_row_number = int(length / (r * math.sqrt(3)))
            count = int(special_row_number / 2) * common_row + int(
                (special_row_number + 1) / 2) * special_row + i * common_row
            if count > max_count:
                max_count = count
                max_c_row = i
                max_s_row = special_row_number
                self.trays[0].clear_tray()
        # 竖着放
        common_row = int(box_l / (2 * r))
        if common_row * 2 * r + r <= box_l:
            special_row = common_row
        else:
            special_row = common_row - 1
        max_row = int(box_w / (2 * r))
        for i in range(max_row):
            i = i + 1
            length = box_w - i * 2 * r
            special_row_number = int(length / (r * math.sqrt(3)))
            count = int(special_row_number / 2) * common_row + int(
                (special_row_number + 1) / 2) * special_row + i * common_row
            if count > max_count:
                max_count = count
                max_c_row = i
                max_s_row = special_row_number
                max_way = 1
                self.trays[0].clear_tray()
        box_count = 0
        if max_way:
            start_h = 2 * r * (max_c_row - 1) + r * math.sqrt(3)
            for i in range(max_c_row):
                for j in range(common_row):
                    if box_count + 1 > len(self.items):
                        break
                    self.items[box_count].position = [j * 2 * r, i * 2 * r, 0]
                    self.trays[0].items.append(self.items[box_count])
                    box_count += 1
                if box_count + 1 > len(self.items):
                    break
            for i in range(max_s_row):
                if i % 2 == 0:
                    for j in range(special_row):
                        if box_count + 1 > len(self.items):
                            break
                        self.items[box_count].position = [j * 2 * r + r, i * math.sqrt(3) * r + start_h, 0]
                        self.trays[0].items.append(self.items[box_count])
                        box_count += 1
                else:
                    for j in range(common_row):
                        if box_count + 1 > len(self.items):
                            break
                        self.items[box_count].position = [j * 2 * r, i * math.sqrt(3) * r + start_h, 0]
                        self.trays[0].items.append(self.items[box_count])
                        box_count += 1
                if box_count + 1 > len(self.items):
                    break
        else:
            start_w = 2 * r * (max_c_row - 1) + r * math.sqrt(3)
            common_row = int(box_w / (2 * r))  # 一行摆多少个
            if common_row * 2 * r + r <= box_w:
                special_row = common_row
            else:
                special_row = common_row - 1
            for i in range(max_c_row):
                for j in range(common_row):
                    if box_count + 1 > len(self.items):
                        break
                    self.items[box_count].position = [i * 2 * r, j * 2 * r, 0]
                    self.trays[0].items.append(self.items[box_count])
                    # print(box_count, self.items[box_count].position)
                    box_count += 1
                if box_count + 1 > len(self.items):
                    break
            for i in range(max_s_row):
                if i % 2 == 0:
                    for j in range(special_row):
                        if box_count + 1 > len(self.items):
                            break
                        self.items[box_count].position = [i * math.sqrt(3) * r + start_w, j * 2 * r + r, 0]
                        self.trays[0].items.append(self.items[box_count])
                        box_count += 1
                else:
                    for j in range(common_row):
                        if box_count + 1 > len(self.items):
                            break
                        self.items[box_count].position = [i * math.sqrt(3) * r + start_w, j * 2 * r, 0]
                        self.trays[0].items.append(self.items[box_count])
                        box_count += 1
                if box_count + 1 > len(self.items):
                    break
        # 各种角度
        min_n = int((box_l - 2 * r) / (math.sqrt(3) * r)) + 2
        max_n = int(box_l / r) - 1
        # max_count = int(box_l / r / 2) * int(box_w / r / 2)
        # print(min_n,max_n)
        for n in range(min_n, max_n + 1):
            # print(box_w,r,n)
            l = (box_l - 2 * r) / (n - 1)
            d = math.sqrt(4 * r * r - l * l)
            row_n = int((box_w - 2 * r) / d) + 1
            if row_n % 2 == 0:
                count = n * row_n / 2
            else:
                count = n * (row_n - 1) / 2 + int((n + 1) / 2)
            if count > max_count:
                max_count = int(count)
                num_1 = int((n + 1) / 2)
                num_2 = n - num_1
                row = 1
                for i in range(max_count):
                    if row % 2 == 1:
                        self.items[i].position = [(i - (row - 1) / 2 * n) * 2 * l, (row - 1) * d, 0]
                        # self.trays[0].items.append(self.items[i])
                        if i % n == num_1 - 1:
                            row += 1
                    else:
                        self.items[i].position = [l + (i - num_1 - n * (row / 2 - 1)) * 2 * l,
                                                  d + 2 * d * (row / 2 - 1), 0]
                        # self.trays[0].items.append(self.items[i])
                        if i % n == n - 1:
                            row += 1
                self.trays[0].clear_tray()
                for i in range(max_count):
                    self.trays[0].items.append(self.items[i])
        # if max_count == int(box_l / (2 * r)) * int(box_w / (2 * r)):
        #     for i in range(max_count):
        #         # print(i)
        #         self.items[i].position = [(i % int(box_l / (2 * r))) * 2 * r, int(i / int(box_l / (2 * r))) * 2 * r, 0]
        #         self.trays[0].items.append(copy.deepcopy(self.items[i]))

        self.items = self.items[:-20]
        return max_count

    def pack_all_items(self):
        tem_number = self.pack_cylinder2()
        target_number = len(self.items)
        try_count = 0
        change_extent = 8
        trend = 0
        shift = 0
        while tem_number < target_number or (tem_number != target_number and try_count < 20):
            try_count += 1
            self.trays[0].clear_tray()
            if tem_number < target_number:
                if trend == -1:
                    change_extent /= 2
                self.trays[0].length += change_extent
                self.trays[0].width += change_extent
                shift += change_extent
            else:
                if trend == 1:
                    change_extent /= 2
                self.trays[0].length -= change_extent
                self.trays[0].width -= change_extent
                shift -= change_extent
            tem_number = self.pack_cylinder2()
        while len(self.trays[0].items) > target_number:
            self.trays[0].items.pop()
        self.trays[0].reset_tray()

    def pack(self, bigger_first=True, distribute_items=True, fix_point=True, check_stable=False,
             support_surface_ratio=0.75, binding=[], number_of_decimals=DEFAULT_NUMBER_OF_DECIMALS):
        '''pack master func '''
        # set decimals
        # for bin in self.bins:
        #     bin.formatNumbers(number_of_decimals)
        # for item in self.items:
        #     item.formatNumbers(number_of_decimals)
        # add binding attribute
        self.binding = binding
        # Bin : sorted by volumn
        self.bins.sort(key=lambda bin: bin.getVolume(), reverse=bigger_first)
        # Item : sorted by volumn -> sorted by loadbear -> sorted by level -> binding
        self.items.sort(key=lambda item: item.getVolume(), reverse=bigger_first)
        # self.items.sort(key=lambda item: item.getMaxArea(), reverse=bigger_first)
        self.items.sort(key=lambda item: item.level, reverse=False)
        # sorted by binding
        if binding != []:
            self.sortBinding(bin)

        for idx, bin in enumerate(self.bins):
            # pack item to bin
            for item in self.items:
                self.pack2Bin(bin, item, fix_point, check_stable, support_surface_ratio)

            if binding != []:
                # resorted
                self.items.sort(key=lambda item: item.getVolume(), reverse=bigger_first)
                self.items.sort(key=lambda item: item.loadbear, reverse=True)
                self.items.sort(key=lambda item: item.level, reverse=False)
                # clear bin
                bin.items = []
                bin.unfitted_items = self.unfit_items
                bin.fit_items = np.array([[0, bin.width, 0, bin.height, 0, 0]])
                # repacking
                for item in self.items:
                    self.pack2Bin(bin, item, fix_point, check_stable, support_surface_ratio)

            # Deviation Of Cargo Gravity Center 
            # self.bins[idx].gravity = self.gravityCenter(bin)

            if distribute_items:
                for bitem in bin.items:
                    no = bitem.partno
                    for item in self.items:
                        if item.partno == no:
                            self.items.remove(item)
                            break

        # put order of items
        # self.putOrder()

        if self.items != []:
            self.unfit_items = copy.deepcopy(self.items)
            self.items = []

    def pack_by_sequence(self):
        # 按顺序加入货物
        self.items.sort(key=lambda item: item.height, reverse=True)
        self.items.sort(key=lambda item: item.level, reverse=False)
        count = 0
        for i in range(len(self.bins)):
            y = 0
            x = 0
            whole_tray_length = self.items[count].length
            whole_tray_width = self.items[count].width
            for j in range(self.bins[i].max_whole_number):
                item = self.items[count]
                if item.height != 0:
                    item.position = [y, x, 0]
                    if j % 2 == 0:
                        x = whole_tray_width
                    else:
                        x = 0
                        y += whole_tray_length
                    self.bins[i].items.append(item)
                count += 1
        return 0


class Painter:
    def __init__(self, thing):
        if type(thing) == Bin:
            self.items = thing.items
            self.length = thing.length
            self.width = thing.width
            self.height = thing.height
            self.patch_zu = ()
            self.label_zu = ()
        else:
            self.items = thing.items
            self.length = thing.length
            self.width = thing.width
            self.height = thing.height
            self.tray = thing
            self.patch_zu = ()
            self.label_zu = ()

    def _plotCube(self, ax, x, y, z, dx, dy, dz, color='red', mode=2, linewidth=1, text="", fontsize=15, alpha=0.5,
                  is_tray=0):
        global patch_zu
        global label_zu
        global same_box
        global now_box
        global new_bin
        """ Auxiliary function to plot a cube. code taken somewhere from the web.  """
        xx = [x, x, x + dx, x + dx, x]
        yy = [y, y + dy, y + dy, y, y]

        kwargs = {'alpha': 1, 'color': color, 'linewidth': linewidth}
        if mode == 1:
            ax.plot3D(xx, yy, [z] * 5, **kwargs)
            ax.plot3D(xx, yy, [z + dz] * 5, **kwargs)
            ax.plot3D([x, x], [y, y], [z, z + dz], **kwargs)
            ax.plot3D([x, x], [y + dy, y + dy], [z, z + dz], **kwargs)
            ax.plot3D([x + dx, x + dx], [y + dy, y + dy], [z, z + dz], **kwargs)
            ax.plot3D([x + dx, x + dx], [y, y], [z, z + dz], **kwargs)
        else:
            p = Rectangle((x, y), dx, dy, fc=color, ec='black', alpha=alpha)
            p2 = Rectangle((x, y), dx, dy, fc=color, ec='black', alpha=alpha)
            p3 = Rectangle((y, z), dy, dz, fc=color, ec='black', alpha=alpha)
            p4 = Rectangle((y, z), dy, dz, fc=color, ec='black', alpha=alpha)
            p5 = Rectangle((x, z), dx, dz, fc=color, ec='black', alpha=alpha)
            p6 = Rectangle((x, z), dx, dz, fc=color, ec='black', alpha=alpha)
            ax.add_patch(p)
            ax.add_patch(p2)
            ax.add_patch(p3)
            ax.add_patch(p4)
            ax.add_patch(p5)
            ax.add_patch(p6)
            if (same_box == False or new_bin) and is_tray == False:
                self.patch_zu += (p,)
                self.label_zu += (now_box,)
                new_bin = False

            if text != "":
                ax.text((x + dx / 2), (y + dy / 2), (z + dz / 2), str(text), color='black', fontsize=fontsize,
                        ha='center', va='center')

            art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
            art3d.pathpatch_2d_to_3d(p2, z=z + dz, zdir="z")
            art3d.pathpatch_2d_to_3d(p3, z=x, zdir="x")
            art3d.pathpatch_2d_to_3d(p4, z=x + dx, zdir="x")
            art3d.pathpatch_2d_to_3d(p5, z=y, zdir="y")
            art3d.pathpatch_2d_to_3d(p6, z=y + dy, zdir="y")

    def _plotCylinder(self, ax, x, y, z, dx, dy, dz, color='red', mode=2, text="", fontsize=10, alpha=0.2):
        global patch_zu
        global label_zu
        global same_box
        global now_box
        """ Auxiliary function to plot a Cylinder  """
        # plot the two circles above and below the cylinder
        kwargs = {'alpha': alpha, 'facecolor': color, 'linewidth': 1}
        p = Circle((x + dx / 2, y + dy / 2), radius=dx / 2, edgecolor=color, **kwargs)
        kwargs = {'alpha': 0.5, 'facecolor': color, 'linewidth': 1}
        ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
        # plot a circle in the middle of the cylinder
        center_z = np.linspace(0, dz, 2)
        theta = np.linspace(0, 2 * np.pi, 10)
        theta_grid, z_grid = np.meshgrid(theta, center_z)  # 生成网格
        x_grid = dx / 2 * np.cos(theta_grid) + x + dx / 2
        y_grid = dy / 2 * np.sin(theta_grid) + y + dy / 2
        z_grid = z_grid + z
        ax.plot_surface(x_grid, y_grid, z_grid, shade=True, fc=color, alpha=alpha, color=color)
        if text != "":
            ax.text((x + dx / 2), (y + dy / 2), (z + dz / 2), str(text), color='black', fontsize=fontsize, ha='center',
                    va='center')

    def plotTrayAndItems(self, title="", alpha=0.2, fontsize=10, packer_count=0, tray_color="yellow", shift=0):
        fig = plt.figure()
        axGlob = plt.axes(projection='3d')
        for item in self.items:
            x, y, z = item.position
            [l, w, h] = item.getDimension()
            color = item.color
            text = item.partno
            # plot item of cylinder
            self._plotCylinder(axGlob, float(x) + shift, float(y) + shift, float(z), float(l), float(w), float(h),
                               color=color,
                               mode=2, text=text, fontsize=fontsize, alpha=alpha)
        self._plotCube(axGlob, self.tray.extra_length / 2, self.tray.extra_width / 2, -float(self.height),
                       float(self.length - self.tray.extra_length), float(self.width - self.tray.extra_width),
                       float(self.height),
                       color=tray_color,
                       mode=2, fontsize=fontsize, alpha=0.2)
        plt.title(title)
        self.setAxesEqual(axGlob)
        return plt

    def plotBoxAndItems(self, title="", alpha=0.2, write_num=False, fontsize=10, plotbox=1):
        global patch_zu
        global label_zu
        global same_box
        global now_box
        global new_bin
        """ side effective. Plot the Bin and the items it contains. """
        fig = plt.figure(figsize=(20, 20))
        axGlob = plt.axes(projection='3d')

        # plot bin
        new_bin = True
        if plotbox:
            self._plotCube(axGlob, 0, 0, 0, float(self.length), float(self.width), float(self.height), color='black',
                           mode=1, linewidth=2, text="")
        counter = 0
        # fit rotation type
        for item in self.items:
            rt = item.rotation_type
            x, y, z = item.position
            [w, h, d] = item.getDimension()
            color = item.color
            text = item.partno if write_num else ""
            if now_box == item.partno:
                same_box = True
            else:
                same_box = False
            now_box = item.partno

            if type(item) == Tray:
                self._plotCube(axGlob, float(x), float(y), float(z), float(w), float(h), float(d), color=color, mode=2,
                               text=text, fontsize=fontsize, alpha=0.3, is_tray=1)
            else:
                if item.typeof == 'cube':
                    # plot item of cube
                    self._plotCube(axGlob, float(x), float(y), float(z), float(w), float(h), float(d), color=color,
                                   mode=2, text=text, fontsize=fontsize, alpha=alpha)
                elif item.typeof == 'cylinder':
                    # plot item of cylinder
                    self._plotCylinder(axGlob, float(x), float(y), float(z), float(w), float(h), float(d), color=color,
                                       mode=2, text=text, fontsize=fontsize, alpha=alpha)
            counter = counter + 1
        plt.title(title)
        self.setAxesEqual(axGlob)
        return plt

    def setAxesEqual(self, ax):
        '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
        cubes as cubes, etc..  This is one possible solution to Matplotlib's
        ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

        Input
        ax: a matplotlib axis, e.g., as output from plt.gca().'''
        x_limits = ax.get_xlim3d()
        y_limits = ax.get_ylim3d()
        z_limits = ax.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = np.mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = np.mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = np.mean(z_limits)

        # The plot bounding box is a sphere in the sense of the infinity
        # norm, hence I call half the max range the plot radius.
        plot_radius = 0.5 * max([x_range, y_range, z_range])

        ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


class PackerHandler:
    def __init__(self, packer, packer_count, unfit_item_list, unfit_item_number, mixed_count, fig):
        self.packer = packer
        self.packer_count = packer_count
        self.unfit_item_list = unfit_item_list
        self.unfit_item_number = unfit_item_number
        self.mixed_count = mixed_count
        self.fig = fig

    def mixed_items_pack_as_same(self, items_number_in_a_tray_r, items_number_in_a_tray_n, tray, foam_height, task_id):
        tray0 = copy.deepcopy(tray)
        i = 0
        number = 1
        unfit_radius = []
        mix_as_same_count = 0
        self.unfit_item_list.reverse()
        self.unfit_item_number.reverse()
        self.packer[0].unfit_items.reverse()
        for item in self.unfit_item_list:
            unfit_radius.append(item.length / 2)
        print('开始规则混装')
        print(unfit_radius)
        print(self.unfit_item_number)
        print(f'规格表-半径{items_number_in_a_tray_r}')
        print(f'规格表-数量{items_number_in_a_tray_n}')
        # 检视需要混装的货物
        while i < len(self.packer[0].unfit_items):
            now_r = self.packer[0].unfit_items[i].width / 2
            find_flag = False
            for j in range(len(items_number_in_a_tray_r)):
                if abs(items_number_in_a_tray_r[j] - now_r) < 0.0001:
                    number = same_r_number_in_list(unfit_radius, self.unfit_item_number, now_r)
                    # 剩余量为0时变为1使i累加
                    if number == 0:
                        number = 1
                        break
                    # 同种半径不同高度的货物有足够数量可以凑成一托
                    if number >= items_number_in_a_tray_n[j]:
                        weight_count = 0
                        level_count = 0
                        pack_item = []
                        self.mixed_count += 1
                        max_height = self.packer[0].unfit_items[i].height
                        max_radius = self.packer[0].unfit_items[i].width / 2
                        self.packer.append(Packer())
                        self.packer_count += 1
                        tray0.clear_tray()
                        self.packer[self.packer_count].trays.append(tray0)
                        # 减去相应个数的货物，新增的任务增加相应个数
                        count = items_number_in_a_tray_n[j]
                        while count:
                            count -= 1
                            # print(len(self.packer[0].unfit_items), i)
                            self.packer[self.packer_count].items.append(copy.deepcopy(self.packer[0].unfit_items[i]))
                            weight_count += self.packer[0].unfit_items[i].weight
                            level_count += self.packer[0].unfit_items[i].level
                            pack_item.append(self.packer[0].unfit_items[i])
                            self.packer[0].unfit_items.pop(i)
                        level = level_count / items_number_in_a_tray_n[j]
                        n_list_reduce_by_r(unfit_radius, self.unfit_item_number, now_r, items_number_in_a_tray_n[j])
                        find_flag = True
                        mix_as_same_count += 1
                        self.packer[0].addItem(Item(
                            # partno=f'混装托盘{self.mixed_count}({max_height - foam_height / 10})',
                            partno=f"混装托盘",
                            name="name",
                            typeof="cube",
                            lwh=[tray0.length, tray0.width, max_height + tray0.height],
                            weight=weight_count + tray0.weight, level=level, updown=False, color="yellow", is_mixed=True,
                            pack_item=pack_item
                        ))
                        self.packer[self.packer_count].pack_all_items()
                        # self.packer[self.packer_count].pack_cylinder2()
                        save_path = create_and_save_plot(self.packer[self.packer_count].trays[0],
                                                         task_id, f'{item_list2name(pack_item)}')
                        self.packer[0].items[-1].address = save_path
                        self.fig.append(
                            Painter(self.packer[self.packer_count].trays[0]).
                            plotTrayAndItems(alpha=0.9, fontsize=10,
                                             title=f'混装托盘{self.mixed_count}',
                                             packer_count=self.packer_count))
                    break
            if not find_flag:
                i += number
        print(f'规则装托共装{mix_as_same_count}个小托')
        return [self.packer, self.packer_count, self.unfit_item_list, self.unfit_item_number,
                self.mixed_count, self.fig]


class AddBinToPacker:
    def __init__(self, packer, bin_count, bin_v_count, max_whole_tray_number, fig):
        self.packer = packer  # 初始化时添加一个 Packer
        self.bin_count = bin_count
        self.bin_v_count = bin_v_count
        self.max_whole_tray_number = max_whole_tray_number
        self.fig = fig

    def add_bin_to_packer(self, bin_name, bin_number, bin_length, bin_width, bin_height, bin_max_weight, tray_length,
                          tray_width, print_info):
        # max_weight_count = 0
        bin_load_weight_list = []
        bin_load_number_list = []
        for i in range(len(bin_name)):
            n = int((bin_length[i] // tray_length) * (bin_width[i] // tray_width))
            for j in range(bin_number[i]):
                box = Bin(partno=bin_name[i] + str(j + 1), lwh=[bin_length[i], bin_width[i], bin_height[i]], put_type=0,
                          max_weight=bin_max_weight[i], max_whole_number=n)
                self.packer[0].addBin(box)
                self.packer.append(Packer())
                self.packer[self.bin_count + j + 1].addBin(box)
                self.fig.append(1)
                bin_load_weight_list.append(bin_max_weight[i])
                bin_load_number_list.append(int((bin_length[i] // tray_length) * (bin_width[i] // tray_width)))
                print_info.append(f'托盘规格为{tray_length}*{tray_width}\n')

            self.bin_count += bin_number[i]
            self.bin_v_count += bin_length[i] / 100 * bin_width[i] / 100 * bin_height[i] / 100 * bin_number[i]
            # max_weight_count += bin_max_weight[i] * bin_number[i]
            self.max_whole_tray_number += n * bin_number[i]
        return [self.packer, self.bin_count, self.bin_v_count, self.max_whole_tray_number, self.fig,
                bin_load_weight_list, bin_load_number_list, self.bin_count, print_info]


class AddItemToPackerAndPackSame:
    def __init__(self, packer, bin_count, tray, unfit_item_list, unfit_item_number,
                 items_number_in_a_tray_r, items_number_in_a_tray_n, fig):
        self.packer = packer
        self.packer_count = bin_count
        self.tray = tray
        self.unfit_item_list = unfit_item_list
        self.unfit_item_number = unfit_item_number
        self.items_number_in_a_tray_r = items_number_in_a_tray_r
        self.items_number_in_a_tray_n = items_number_in_a_tray_n
        self.fig = fig

    def add_item_and_pack_same(self, item_name, item_name_hd, item_hd, item_kd, item_name_cd, item_cd, item_diameter, item_height, item_weight,
                               item_num, item_level, often_thickness, often_length, often_number,
                               element_color, mixed_flag, tray_weight, task_id, ask_time, bin_count, second_input=[]):
        tray_num = []
        number_count = 0
        weight_count = 0
        tray_count = 0
        pre_radius = 0
        result = []
        try_count = 0  # 尝试次数
        j = 0
        # 按优先级排序
        level_idx = np.argsort(item_level, kind="stable")
        item_level = np.array(item_level)
        item_level = item_level[level_idx]
        item_name = np.array(item_name)
        item_name = item_name[level_idx]
        item_name_hd = np.array(item_name_hd)
        item_name_hd = item_name_hd[level_idx]
        item_hd = np.array(item_hd)
        item_hd = item_hd[level_idx]
        item_kd = np.array(item_kd)
        item_kd = item_kd[level_idx]
        item_name_cd = np.array(item_name_cd)
        item_name_cd = item_name_cd[level_idx]
        item_cd = np.array(item_cd)
        item_cd = item_cd[level_idx]
        item_diameter = np.array(item_diameter)
        item_diameter = item_diameter[level_idx]
        item_height = np.array(item_height)
        item_height = item_height[level_idx]
        item_weight = np.array(item_weight)
        item_weight = item_weight[level_idx]
        item_num = np.array(item_num)
        item_num = item_num[level_idx]
        if second_input:
            second_number = [item['number'] for item in second_input["data"]]
            is_changed_list = [item['isChanged'] for item in second_input["data"]]
        # 尝试加入到装箱任务中
        for i in range(len(item_name)):
            number = int(item_num[i])
            weight = item_weight[i] / number
            partno = item_name_hd[i] + '*' + item_kd[i] + '*' + item_name_cd[i]
            weight_count += item_weight[i]
            name = item_name[i]
            diameter = item_diameter[i] / 10
            height = item_height[i] / 10
            level = item_level[i]
            number_count += number
            item = Item(partno=partno, name=name, typeof="cylinder",
                        lwh=[diameter, diameter, height], weight=weight,
                        level=level, updown=False,
                        color=element_color[i % 20])
            # 每种货物装托盘
            if ask_time == 0:
                for j in range(bin_count):
                    self.packer.append(Packer())
            self.packer.append(Packer())
            self.packer_count += 1
            self.tray.clear_tray()
            self.packer[self.packer_count].trays.append(copy.deepcopy(self.tray))
            # 将需要装的同规格货物加入到装箱任务中
            for idx, j in enumerate(range(int(number))):
                self.packer[self.packer_count].items.append(copy.deepcopy(item))
            # item_in_tray_number记录托盘放几个货物,这里是指定一托装载个数
            find_in_often = False
            shift = 0
            if second_input:
                for j in range(len(second_number)):
                    if item_name_hd[i] == second_input["data"][j]["item_hd"] and item_name_cd[i] == second_input["data"][j]["item_cd"]:
                        item_in_tray_number = second_number[j]
                        break
                tem_number = self.packer[self.packer_count].pack_cylinder2()
                try_count = 0
                change_extent = 8
                trend = 0
                while tem_number < item_in_tray_number or (tem_number != item_in_tray_number and try_count < 20):
                    try_count += 1
                    self.packer[self.packer_count].trays[0].clear_tray()
                    if tem_number < item_in_tray_number:
                        if trend == -1:
                            change_extent /= 2
                        self.packer[self.packer_count].trays[0].length += change_extent
                        self.packer[self.packer_count].trays[0].width += change_extent
                        shift += change_extent
                    else:
                        if trend == 1:
                            change_extent /= 2
                        self.packer[self.packer_count].trays[0].length -= change_extent
                        self.packer[self.packer_count].trays[0].width -= change_extent
                        shift -= change_extent
                    tem_number = self.packer[self.packer_count].pack_cylinder2()
                while len(self.packer[self.packer_count].trays[0].items) > item_in_tray_number:
                    self.packer[self.packer_count].trays[0].items.pop()
                self.packer[self.packer_count].trays[0].reset_tray()
            else:
                for j in range(len(often_thickness)):
                    # 表中找到指定厚度与长度且有数据的货物
                    if abs(often_thickness[j] - float(item_name_hd[i])) < 0.001 and abs(often_length[j] - float(item_name_cd[i])) < 0.001 and not pd.isnull(often_number[j]):
                        find_in_often = True
                        item_in_tray_number = float(often_number[j])
                        tem_number = self.packer[self.packer_count].pack_cylinder2()
                        try_count = 0
                        change_extent = 8
                        trend = 0
                        while tem_number < item_in_tray_number or (
                                tem_number != item_in_tray_number and try_count < 20):
                            try_count += 1
                            self.packer[self.packer_count].trays[0].clear_tray()
                            if tem_number < item_in_tray_number:
                                if trend == -1:
                                    change_extent /= 2
                                self.packer[self.packer_count].trays[0].length += change_extent
                                self.packer[self.packer_count].trays[0].width += change_extent
                                shift += change_extent
                            else:
                                if trend == 1:
                                    change_extent /= 2
                                self.packer[self.packer_count].trays[0].length -= change_extent
                                self.packer[self.packer_count].trays[0].width -= change_extent
                                shift -= change_extent
                            tem_number = self.packer[self.packer_count].pack_cylinder2()
                        # ??????
                        while len(self.packer[self.packer_count].trays[0].items) > item_in_tray_number:
                            self.packer[self.packer_count].trays[0].items.pop()
                        self.packer[self.packer_count].trays[0].reset_tray()
                        break
                if not find_in_often:
                    item_in_tray_number = self.packer[self.packer_count].pack_cylinder2()
                if i == 0 or (item_name_hd[i] != item_name_hd[i-1] or item_name_cd[i] != item_name_cd[i-1]):
                    result.append({'item_hd': item_name_hd[i], 'item_cd': item_name_cd[i],
                                   'often_number': int(often_number[j]) if find_in_often else None,
                                   'number': item_in_tray_number})

            # tray_num列表记录每种货物几个小托，unfitted_items记录剩下的货物
            if ask_time:
                if mixed_flag:
                    tray_num.append(int(number / item_in_tray_number))
                    remain_num = number - item_in_tray_number * tray_num[tray_count]
                    if remain_num == 0:
                        print(partno, "一托装", item_in_tray_number, "个，共装", int(number / item_in_tray_number), "托")
                    else:
                        print(partno, "一托装", item_in_tray_number, "个，共装", int(number / item_in_tray_number),
                              "托，剩余", remain_num, "个该货物")
                else:
                    tray_num.append(math.ceil(number / item_in_tray_number))
                    remain_num = number % item_in_tray_number
                    if remain_num == 0:
                        print(partno, "一托装", item_in_tray_number, "个，共装", tray_num[-1], "托")
                    else:
                        print(partno, "一托装", item_in_tray_number, "个，共装", tray_num[-1], "托，最后一托装载",
                              remain_num, "个该货物")
            tray_count += 1
            # 同规格装托盘后剩余货物先放在packer[0]中
            if ask_time == 1:
                if remain_num != 0 and mixed_flag == False:
                    temp_tray = copy.deepcopy(self.packer[self.packer_count].trays[0])
                    while len(temp_tray.items) > remain_num:
                        temp_tray.items.pop()
                    save_path_0 = create_and_save_plot(temp_tray, task_id, partno)
                save_path = create_and_save_plot(self.packer[self.packer_count].trays[0], task_id, partno)
                if mixed_flag:
                    item0 = Item(partno=partno, name=name, typeof="cylinder",
                                 lwh=[diameter, diameter, height], weight=weight, level=1,
                                 updown=False, color=element_color[i % 20])
                    for j in range(int(remain_num)):
                        self.packer[0].unfit_items.append(item0)
                    self.unfit_item_list.append(item0)
                    self.unfit_item_number.append(remain_num)
                    if abs(pre_radius - diameter / 2) > 0.0001:
                        self.fig.append(
                            Painter(self.packer[self.packer_count].trays[0]).
                            plotTrayAndItems(alpha=0.9, fontsize=10, title=partno, packer_count=self.packer_count,
                                             shift=-shift // 2))
                        pre_radius = diameter / 2
                        self.items_number_in_a_tray_r.append(pre_radius)
                        self.items_number_in_a_tray_n.append(item_in_tray_number)
                    # elif item_in_tray_number!=

                # 将装好的托盘变为一个整体货物装入pack0中
                for j in range(tray_num[-1]):
                    if remain_num == 0 or mixed_flag or j != tray_num[-1] - 1:
                        self.packer[0].addItem(
                            Item(partno=partno + '*' + str(item_in_tray_number), name=name, typeof="cube",
                                 lwh=[self.tray.length - self.tray.extra_length,
                                      self.tray.width - self.tray.extra_width, height + self.tray.height],
                                 weight=weight * item_in_tray_number + tray_weight, level=level, address=save_path,
                                 updown=False, color=element_color[i % 20],
                                 pack_item=[item], pack_item_number=[item_in_tray_number], pack_tray=[]))
                    else:
                        self.packer[0].addItem(
                            Item(partno=partno + '*' + str(remain_num), name=name, typeof="cube",
                                 lwh=[self.tray.length - self.tray.extra_length,
                                      self.tray.width - self.tray.extra_width, height + self.tray.height],
                                 weight=weight * remain_num + tray_weight, level=level,
                                 updown=False, color=element_color[i % 20], is_mixed=True, address=save_path_0,
                                 pack_item=[item], pack_item_number=[remain_num], pack_tray=[]))
                    # self.packer[0].items[-1].address = save_path
        print(f'膜卷货物共{number_count}个')
        print(f'同品名装托共装{len(self.packer[0].items)}个小托')
        if ask_time == 0:
            print(type(result))
            return result
        else:
            n = len(self.unfit_item_list)
            for i in range(n - 1):
                # 内层每次比较相邻两项
                for j in range(n - 1 - i):
                    a = self.unfit_item_list[j]
                    b = self.unfit_item_list[j + 1]
                    if abs(a.length - b.length) < 0.001 and a.height > b.height:
                        self.unfit_item_list[j], self.unfit_item_list[j + 1] = b, a
                        self.unfit_item_number[j], self.unfit_item_number[j + 1] = (
                            self.unfit_item_number[j + 1],
                            self.unfit_item_number[j],
                        )

            n = len(self.packer[0].unfit_items)
            for i in range(n - 1):
                # 内层每次比较相邻两项
                for j in range(n - 1 - i):
                    a = self.packer[0].unfit_items[j]
                    b = self.packer[0].unfit_items[j + 1]
                    if abs(a.length - b.length) < 0.001 and a.height > b.height:
                        self.packer[0].unfit_items[j], self.packer[0].unfit_items[j + 1] = b, a
            return [self.packer, self.packer_count, self.unfit_item_list,
                    self.unfit_item_number, self.items_number_in_a_tray_r, self.items_number_in_a_tray_n, self.fig]


class MixedPacker:
    def __init__(self, packer, tray, packer_count, fig):
        self.packer = packer  # 初始化时添加一个 Packer
        self.tray = tray
        self.packer_count = packer_count
        self.fig = fig

    def pack_mixed_items(self, s_result, foam_height, mixed_count, tray_weight, task_id):
        unfit_count = 0
        count = 0
        pack_item = []
        self.packer[0].unfit_items.sort(key=return_height, reverse=True)
        print(f"不规则装托共装{len(s_result)}个小托")
        for i in range(len(s_result)):
            weight_count = 0
            level_count = 0
            self.packer.append(Packer())
            pack_item = []
            tray = self.tray
            tray.clear_tray()
            self.packer[self.packer_count + i+1].trays.append(copy.deepcopy(tray))

            for j in range(len(s_result[i][2])):
                # 混装
                self.packer[0].unfit_items[j + unfit_count].position = [
                    s_result[i][1][j] - s_result[i][2][j],
                    s_result[i][0][j] - s_result[i][2][j], 0
                ]
                self.packer[i+1 + self.packer_count].items.append(
                    copy.deepcopy(self.packer[0].unfit_items[j + unfit_count]))
                self.packer[i+1 + self.packer_count].trays[0].items.append(
                    copy.deepcopy(self.packer[0].unfit_items[j + unfit_count]))
                weight_count += self.packer[0].unfit_items[count].weight
                level_count += self.packer[0].unfit_items[count].level
                pack_item.append(Item(partno=self.packer[0].unfit_items[count].partno, typeof='cube',
                                      lwh=[self.packer[0].unfit_items[count].length, self.packer[0].unfit_items[count].width, self.packer[0].unfit_items[count].height],
                                      weight=self.packer[0].unfit_items[count].weight))
                count += 1

            self.fig.append(
                Painter(self.packer[i+1 + self.packer_count].trays[0]).plotTrayAndItems(
                    title=f'混装托盘{mixed_count + i + 1}', alpha=0.9, fontsize=10, packer_count=len(self.packer) - 1
                ))
            save_path = create_and_save_plot(self.packer[self.packer_count+i+1].trays[0], task_id, item_list2name(pack_item))

            # 混装后的托盘加入pack0
            self.packer[0].addItem(Item(
                partno=f'混装托盘',
                name=f'混装托盘',
                typeof="cube",
                lwh=[tray.length, tray.width, self.packer[0].unfit_items[unfit_count].height + tray.height],
                weight=weight_count + tray_weight, level=level_count / len(s_result[i][2]), updown=False,
                color="yellow", is_mixed=True,
                pack_item=pack_item, address=save_path
            ))

            unfit_count += len(s_result[i][2])
        print("共使用", mixed_count + len(s_result), "个托盘进行混装")
        print(' ')
        return [self.packer, self.packer_count, self.fig]


class OverlapHandler:
    def __init__(self, packer):
        self.packer = packer

    def handle_overlap(self, tray_length, tray_width, tray_height, tray_weight, overlap_height, overlap_total_height,
                       overlap_flag, foam_height):
        foam_height /= 10
        if overlap_flag:
            print("膜叠膜处理：")
            self.packer[0].items.sort(key=return_height0, reverse=True)
            if not self.packer[0].items:
                return self.packer
            item_list = []
            now_tray = self.packer[0].items[0]
            h_count = now_tray.height - tray_height  # h_count统计未加上托盘的总高度
            weight_count = now_tray.weight - tray_weight  # 同上
            pack_tray_list = []
            count = 1
            overlap_count = 0

            for j in range(1, len(self.packer[0].items)):
                i = self.packer[0].items[j]
                if i.is_mixed:
                    if count > 1:
                        item_list.append(Item(partno=now_tray.partno + '(*' + str(count) + ')', typeof="cube",
                                              lwh=[tray_length, tray_width, tray_height + h_count],
                                              weight=weight_count + tray_weight, level=now_tray.level,
                                              is_mixed=now_tray.is_mixed, is_overlap=True,
                                              pack_tray=pack_tray_list, pack_item=now_tray.pack_item, pack_item_number=[x * count for x in now_tray.pack_item_number],
                                              overlap_layers=count, address=now_tray.address))
                        print(str(count), "层", now_tray.partno, "进行膜叠膜")
                        overlap_count += count - 1
                    else:
                        item_list.append(Item(partno=now_tray.partno, typeof="cube",
                                              lwh=[tray_length, tray_width, tray_height + h_count],
                                              weight=weight_count + tray_weight, level=now_tray.level,
                                              is_mixed=now_tray.is_mixed,
                                              pack_tray=pack_tray_list, pack_item=now_tray.pack_item, pack_item_number=now_tray.pack_item_number,
                                              address=now_tray.address))
                    now_tray = i
                    h_count = now_tray.height - tray_height
                    weight_count = now_tray.weight - tray_weight
                    # pack_tray_list = []
                    count = 1
                else:
                    base_goods_height = now_tray.height - tray_height - foam_height
                    candidate_goods_height = i.height - tray_height - foam_height
                    stacked_goods_height = h_count - count * foam_height
                    if can_stack_layer(
                            now_tray.partno, i.partno, now_tray.is_mixed, i.is_mixed,
                            base_goods_height, candidate_goods_height, stacked_goods_height,
                            overlap_height, overlap_total_height):
                        h_count += i.height - tray_height
                        weight_count += i.weight - tray_weight
                        # pack_tray_list.append(i)
                        count += 1
                    else:
                        if count > 1:
                            item_list.append(Item(partno=now_tray.partno + '(*' + str(count) + ')', typeof="cube",
                                                  lwh=[tray_length, tray_width, tray_height + h_count],
                                                  weight=weight_count + tray_weight, level=now_tray.level,
                                                  is_mixed=False, is_overlap=True, pack_tray=pack_tray_list,
                                                  pack_item=now_tray.pack_item, pack_item_number=[x * count for x in now_tray.pack_item_number],
                                                  overlap_layers=count, address=now_tray.address))
                            print(str(count), "层", now_tray.partno, "进行膜叠膜")
                            overlap_count += count - 1
                        else:
                            item_list.append(Item(partno=now_tray.partno, typeof="cube",
                                                  lwh=[tray_length, tray_width, tray_height + h_count],
                                                  weight=weight_count + tray_weight, level=now_tray.level,
                                                  is_mixed=False, pack_tray=pack_tray_list,
                                                  pack_item=now_tray.pack_item, pack_item_number=now_tray.pack_item_number, address=now_tray.address))
                        now_tray = i
                        h_count = now_tray.height - tray_height
                        weight_count = now_tray.weight - tray_weight
                        pack_tray_list = []
                        count = 1
            if count > 1:
                item_list.append(Item(partno=now_tray.partno + '(*' + str(count) + ')', typeof="cube",
                                      lwh=[tray_length, tray_width, tray_height + h_count],
                                      weight=weight_count + tray_weight, level=now_tray.level,
                                      is_mixed=False, is_overlap=True, pack_tray=pack_tray_list,
                                      pack_item=now_tray.pack_item,
                                      pack_item_number=[x * count for x in now_tray.pack_item_number],
                                      overlap_layers=count, address=now_tray.address))
                overlap_count += count - 1
            else:
                item_list.append(Item(partno=now_tray.partno, typeof="cube",
                                      lwh=[tray_length, tray_width, tray_height + h_count],
                                      weight=weight_count + tray_weight, level=now_tray.level,
                                      is_mixed=now_tray.is_mixed,
                                      pack_tray=pack_tray_list, pack_item=now_tray.pack_item,
                                      pack_item_number=[x * count for x in now_tray.pack_item_number], address=now_tray.address))
            self.packer[0].items = item_list
            print(f'由于膜叠膜，少使用了{overlap_count}个托盘')
            # print(' ')
            # print("膜叠膜后装货托盘如下：")
            # for i in range(len(self.packer[0].items)):
            #     print(self.packer[0].items[i].partno)
            # print(' ')
        return self.packer


class TrayToWholeTray:
    def __init__(self, packer, tray):
        self.packer = packer
        self.tray = tray

    def tray2whole(self, bin_height, element_color):
        # 混装的pack_item整理
        for item in self.packer[0].items:
            if item.is_mixed:
                item.pack_item_number = []
                item_list = []
                now_item = Item("", "cube", [0, 0, 0], 0)
                for pack_item in item.pack_item:
                    if now_item.partno == pack_item.partno:
                        item.pack_item_number[-1] += 1
                    else:
                        item.pack_item_number.append(1)
                        item_list.append(pack_item)
                        now_item = pack_item
                item.pack_item = copy.deepcopy(item_list)
        self.packer[0].items.sort(key=return_height0, reverse=True)
        self.packer[0].sort_by_partno()

        for i in range(len(self.packer[0].same_r_list)):
            if self.packer[0].same_r_list[i]:  # 半径不是0的情况即非混装
                height_count = 0
                weight_count = 0
                level_count = 0
                count = 0
                tray_list = []
                partno = ''

                while not all_zero_in(self.packer[0].same_r_number[i]):  # 仍存在该半径货物
                    all_check = True
                    for j in range(len(self.packer[0].same_r_number[i])):  # 遍历该半径货物
                        if self.packer[0].same_r_number[i][j] != 0 and \
                                self.packer[0].same_r_item[i][j].height + height_count <= bin_height[0]:
                            height_count += self.packer[0].same_r_item[i][j].height
                            weight_count += self.packer[0].same_r_item[i][j].weight
                            level_count += self.packer[0].same_r_item[i][j].level
                            count += 1
                            tray_list.append(self.packer[0].same_r_item[i][j])
                            self.packer[0].same_r_number[i][j] -= 1
                            if partno:
                                partno += '+'
                            partno += self.packer[0].same_r_item[i][j].partno
                            all_check = False
                            break
                    if all_check:
                        if level_count != 0:
                            self.packer[0].packed_items.append(Item(partno=partno, name=partno, typeof="cube",
                                                                    lwh=[self.tray.length - self.tray.extra_length,
                                                                         self.tray.width - self.tray.extra_width,
                                                                         height_count],
                                                                    weight=weight_count, level=level_count / count,
                                                                    updown=False,
                                                                    color=element_color[0], pack_tray=tray_list))
                        height_count = 0
                        weight_count = 0
                        level_count = 0
                        count = 0
                        tray_list = []
                        partno = ''
                if level_count != 0:
                    self.packer[0].packed_items.append(Item(partno=partno, name=partno, typeof="cube",
                                                            lwh=[self.tray.length - self.tray.extra_length,
                                                                 self.tray.width - self.tray.extra_width,
                                                                 height_count],
                                                            weight=weight_count, level=level_count / count, updown=False,
                                                            color=element_color[0], pack_tray=tray_list))
            # 处理混装,混装在后面进行一次贪心
            else:
                self.packer[0].packed_items.sort(key=return_height0, reverse=True)
                for j in range(len(self.packer[0].same_r_item[i])):  # 遍历混装托盘
                    unfit_flag = True
                    for k in range(len(self.packer[0].packed_items) - j):  # 遍历倒序的整托(排除放好的混装)
                        if self.packer[0].same_r_item[i][j].height + self.packer[0].packed_items[k].height <= \
                                bin_height[0]:
                            self.packer[0].packed_items[k].height += self.packer[0].same_r_item[i][j].height
                            self.packer[0].packed_items[k].partno += '+' + self.packer[0].same_r_item[i][j].partno
                            self.packer[0].packed_items[k].pack_tray.append(
                                self.packer[0].same_r_item[i][j])
                            self.packer[0].packed_items[k].is_mixed = True
                            unfit_flag = False
                            break
                    if unfit_flag:
                        self.packer[0].packed_items.append(copy.deepcopy(self.packer[0].same_r_item[i][j]))
                        self.packer[0].packed_items[-1].pack_tray = [copy.deepcopy(self.packer[0].packed_items[-1])]
        return self.packer


class OptimizePacking:
    def __init__(self, packer, bin_length, bin_width, bin_height, bin_number, tray, max_whole_tray_number,
                 loading_rule, task_id):
        self.packer = packer
        self.bin_height = bin_height
        self.max_height_list = []
        if loading_rule == 1:
            height_count = 0
            max_height_count = 0
            for i in range(len(packer[0].packed_items)):
                height_count += packer[0].packed_items[i].height
            for i in range(len(bin_height)):
                for j in range(bin_number[i]):
                    max_height_count += bin_height[i]
            aver_percentage = height_count / max_height_count
            for i in range(len(bin_height)):
                for j in range(bin_number[i] * int(bin_length[i] // tray.length) * int(bin_width[i] // tray.width)):
                    self.max_height_list.append(int(bin_height[i] * aver_percentage))
        else:
            for i in range(len(bin_height)):
                for j in range(bin_number[i] * int(bin_length[i] // tray.length) * int(bin_width[i] // tray.width)):
                    self.max_height_list.append(bin_height[i])
        self.max_whole_tray_number = max_whole_tray_number
        self.task_id = task_id

    def optimize_packing(self, tray, rule, bin_load_weight_list, bin_load_number_list, overlap_flag, tray_height, tray_weight, lying_flag, lying_order_limit):
        # 混装的pack_item整理
        for item in self.packer[0].items:
            if item.is_mixed:
                item.pack_item_number = []
                item_list = []
                now_item = Item("", "cube", [0, 0, 0], 0)
                for pack_item in item.pack_item:
                    if now_item.partno == pack_item.partno:
                        item.pack_item_number[-1] += 1
                    else:
                        item.pack_item_number.append(1)
                        item_list.append(pack_item)
                        now_item = pack_item
                item.pack_item = copy.deepcopy(item_list)
        self.packer[0].items.sort(key=return_height0, reverse=True)
        self.packer[0].sort_by_partno()

        self.packer[0].packed_items = self.packer[0].items
        whole_tray_number = len(self.packer[0].packed_items)
        self.packer[0].packed_items.sort(key=return_height, reverse=True)
        stop_flag = False
        self.packer[0].unfit_items = []
        # 全拆
        for i in range(len(self.packer[0].packed_items) - 1, -1, -1):
            if len(self.packer[0].packed_items[i].pack_tray) > 1:
                for item in self.packer[0].packed_items[i].pack_tray:
                    self.packer[0].packed_items.append(copy.deepcopy(item))
                self.packer[0].packed_items.pop(i)

        # 货物再排序，先高度低到高（防止出现低的能装却舍弃）
        if lying_flag:
            # return_rate_of_height_s = partial(return_rate_of_height, height=lying_limit)
            # self.packer[0].packed_items = sorted(self.packer[0].packed_items, key=return_rate_of_height_s, reverse=False)
            low_items = [item for item in self.packer[0].packed_items if item.height <= lying_order_limit]
            high_items = [item for item in self.packer[0].packed_items if item.height > lying_order_limit]
            low_items.sort(key=lambda x: x.height)  # 低到高
            high_items.sort(key=lambda x: x.height, reverse=True)  # 高到低
            self.packer[0].packed_items = low_items + high_items
        else:
            self.packer[0].packed_items = sorted(self.packer[0].packed_items, key=return_height, reverse=False)
        # self.packer[0].packed_items = sorted(self.packer[0].packed_items, key=return_level, reverse=False)
        # 首轮优化去除部分货物
        print("首轮优化去除部分货物")
        height_count = 0
        for i in self.packer[0].packed_items:
            height_count += i.height
        while sum_weight(self.packer[0].packed_items) > sum_list(bin_load_weight_list) or height_count > sum_list(self.max_height_list):
            height_count -= self.packer[0].packed_items[-1].height
            self.packer[0].unfit_items.append(self.packer[0].packed_items.pop())
        if not self.packer[0].packed_items:
            self.packer[0].packed_items.append(
                Item('', 'cube', [self.packer[0].unfit_items[0].length, self.packer[0].unfit_items[0].width, 0],
                     0))
        # 少的补一个空的
        for i in range(len(self.packer[0].packed_items), self.max_whole_tray_number):
            self.packer[0].packed_items.append(
                Item('', 'cube', [self.packer[0].packed_items[0].length, self.packer[0].packed_items[0].width, 0], 0))
        # pack_tray为空转为自身
        for item in self.packer[0].packed_items:
            if not item.pack_tray:
                item.pack_tray = [copy.deepcopy(item)]
        # 开始装箱优化
        if len(self.packer[0].packed_items) > self.max_whole_tray_number or rule == "balance":
            dismantle_flag = True
            if rule == "balance":
                print(f'开始平均高度')
            else:
                print(f'整托数量{whole_tray_number}超出限制{self.max_whole_tray_number},开始优化')
            packed_items = copy.deepcopy(self.packer[0].packed_items)
            dis_overlap_count = len(packed_items) - 1
            before_dismantle_items = packed_items
            pre_over_height_sum = 10000
            appoint_flag = False
            while True:
                # 多余托盘加到之前整托上
                print("多余托盘加到之前整托上")
                count = 0
                stop_flag = False
                while len(self.packer[0].packed_items) > self.max_whole_tray_number:
                    if not self.packer[0].packed_items[count].is_mixed or not self.packer[0].packed_items[-1].is_mixed:
                        if self.packer[0].packed_items[-1].is_mixed:
                            self.packer[0].packed_items[count].is_mixed = True
                            self.packer[0].packed_items[count].pack_tray += self.packer[0].packed_items[-1].pack_tray
                        else:
                            self.packer[0].packed_items[count].pack_tray = self.packer[0].packed_items[-1].pack_tray + \
                                                                           self.packer[0].packed_items[count].pack_tray
                        self.packer[0].packed_items[count].height += self.packer[0].packed_items[-1].height
                        self.packer[0].packed_items[count].weight += self.packer[0].packed_items[-1].weight
                        self.packer[0].packed_items.pop()
                    count = (count + 1) % self.max_whole_tray_number
                # 进行贪心
                print("开始贪心")
                while not stop_flag:
                    stop_flag = True  # 如果一整轮没有发生交换就停止
                    for i in range(self.max_whole_tray_number):  # 正在贪心交换的整托
                        best_get_score = 0
                        best_programme = [0, 0, 0, 0]
                        for j in range(self.max_whole_tray_number):  # 与之交换的整托
                            if i != j:
                                pre_score = get_score(self.packer[0].packed_items[i], self.max_height_list[i], rule) + \
                                            get_score(self.packer[0].packed_items[j], self.max_height_list[j], rule)
                                whole_tray1, whole_tray2, programme = \
                                    best_exchange_in(self.packer[0].packed_items[i], self.packer[0].packed_items[j],
                                                     self.max_height_list[i], self.max_height_list[j], rule)
                                now_score = get_score(whole_tray1, self.max_height_list[i], rule) + get_score(
                                    whole_tray2, self.max_height_list[j], rule)
                                if now_score - pre_score > best_get_score:
                                    best_programme = [i, j] + programme
                                    best_get_score = now_score - pre_score
                        # if not all_zero_in(best_programme):
                        # print(best_programme, best_get_score)
                        flag = list_exchange_by_programme(self.packer[0].packed_items, best_programme)
                        # print(best_programme)
                        if flag:
                            stop_flag = False
                print("结束贪心")
                # 整托全部小于要求高度结束
                over_height_flag = False
                over_weight_flag = False
                bin_count = 0
                weight_count = 0
                whole_tray_count = 0
                # 统计超高量和超高超重标志
                over_height_sum = 0
                for i in range(self.max_whole_tray_number):
                    if self.packer[0].packed_items[i].height > self.max_height_list[i]:
                        over_height_flag = True
                        over_height_sum += self.packer[0].packed_items[i].height - self.max_height_list[i]
                    whole_tray_count += 1
                    weight_count += self.packer[0].packed_items[i].weight
                    if weight_count > bin_load_weight_list[bin_count]:
                        over_weight_flag = True
                    if whole_tray_count >= bin_load_number_list[bin_count]:
                        whole_tray_count = 0
                        weight_count = 0
                        bin_count += 1
                if not over_height_flag and not over_weight_flag:
                    # 不超高超重则完成优化
                    break
                else:
                    if packed_items[-1].height == 0:
                        packed_items.pop()
                    else:
                        if appoint_flag:
                            appoint_flag = False
                        else:
                            # 效果好就继续拆，不好就回退（评定方式为统计超出上限的高度累加
                            if over_height_sum <= pre_over_height_sum:
                                dismantle_flag = True
                            else:
                                dismantle_flag = False
                                packed_items = before_dismantle_items
                                appoint_flag = True
                        pre_over_height_sum = over_height_sum
                        # 如果超高 膜叠膜 上次拆效果好 还有膜叠膜货物拆 则尝试拆膜叠膜货物
                        if over_height_flag and overlap_flag and dismantle_flag and dis_overlap_count:
                            # 每次重新从尾开始找拆的货物
                            dis_overlap_count = len(packed_items) - 1
                            before_dismantle_items = packed_items
                            # 从后往前拆，即先拆高的
                            while dis_overlap_count:
                                item = packed_items[dis_overlap_count]
                                if item.is_overlap:
                                    print(f'拆解第{dis_overlap_count}个货物{item.partno},拆后总高度为{sum_height(packed_items)}')
                                    item.height = (item.height - tray_height)/item.overlap_layers + tray_height
                                    item.is_overlap = False
                                    item.pack_item_number[0] /= item.overlap_layers
                                    item.partno = item.partno[0:item.partno.find('(')]
                                    item.weight = (item.weight-tray_weight)/item.overlap_layers + tray_weight
                                    item.pack_tray = [copy.deepcopy(item)]
                                    for overlap_count in range(item.overlap_layers):
                                        packed_items.append(copy.deepcopy(item))
                                    packed_items.pop(dis_overlap_count)
                                    break
                                else:
                                    dis_overlap_count -= 1
                        else:
                            dismantle_flag = True
                            self.packer[0].unfit_items.append(packed_items.pop())
                            if len(packed_items)-1 < dis_overlap_count:
                                dis_overlap_count -= 1
                            if over_height_flag:
                                print(f"货物过多,去除{self.packer[0].unfit_items[-1].partno}")
                            else:
                                print(f"货物过重,去除{self.packer[0].unfit_items[-1].partno}")
                    self.packer[0].packed_items = copy.deepcopy(packed_items)
                    print(f"还原后个数{len(packed_items)}")
                    for i in range(len(self.packer[0].packed_items), self.max_whole_tray_number):
                        self.packer[0].packed_items.append(
                            Item('', 'cube',
                                 [self.packer[0].packed_items[0].length, self.packer[0].packed_items[0].width, 0],
                                 0))
                    # pack_tray为空转为自身
                    for item in self.packer[0].packed_items:
                        if not item.pack_tray:
                            item.pack_tray = [copy.deepcopy(item)]

        print('完成优化')
        self.packer[0].items = self.packer[0].packed_items
        self.packer[0].pack_by_sequence()
        return self.packer

    def pack_lying_items(self, lying_flag, lying_limit, tray_data, mixed_flag, lying_tray_flag=True):
        # 排序
        # for i in range(len(self.packer[0].bins)):
        #     self.packer[0].bins[i].items.sort(key=return_height, reverse=True)

        tray_data = tray_data["data"]
        tray_length = tray_data['palletLength'] * 100
        tray_width = tray_data['palletWidth'] * 100
        if lying_tray_flag:
            tray_height = tray_data['palletHeight'] * 100
            tray_weight = tray_data['palletWeight']
        else:
            tray_height = 0
            tray_weight = 0

        # 将unfit_items小托信息整理为item_list
        item_list = []
        for item in self.packer[0].unfit_items:
            if item.is_mixed:
                if item.pack_item_number:
                    for i in range(len(item.pack_item_number)):
                        for j in range(int(item.pack_item_number[i])):
                            item_list.append(copy.deepcopy(item.pack_item[i]))
                else:
                    for i in item.pack_item:
                        item_list.append(copy.deepcopy(i))
            else:
                for i in range(int(item.pack_item_number[0])):
                    item_list.append(copy.deepcopy(item.pack_item[0]))

        if lying_flag:
            print("进行横放")
            # 把横放算法中需要的箱体数据提取出来
            lying_box_height_list = []  # 这里的高度是包含托盘的
            residue_item_count = 0
            whole_tray_count = self.max_whole_tray_number - 1
            whole_tray_flag_list = [False] * self.max_whole_tray_number  # false代表可以被使用
            for i in range(len(self.packer[0].items)):
                if self.packer[0].items[i].is_mixed:
                    whole_tray_flag_list[i] = True
                lying_box_height_list.append(self.max_height_list[i]-self.packer[0].items[i].height)
            if mixed_flag:  # 允许混装，横放的货物也可以混装
                print(f"允许混装的横放计算")
                while item_list:
                    if item_list[residue_item_count].height <= tray_length:  # 一个整托对应一个横放
                        if whole_tray_count >= 0:
                            if not whole_tray_flag_list[whole_tray_count]:
                                lying_items_name, item_list, lying_items_height, lying_items_weight, picture_address, placed_item_number, placed_items = (
                                    pack_circles(tray_width, lying_box_height_list[whole_tray_count]-tray_height, tray_length,
                                                 item_list, self.task_id, whole_tray_count, lying_limit=lying_limit))
                                whole_tray_flag_list[whole_tray_count] = True
                                # 如果装入
                                if lying_items_height:
                                    self.packer[0].items[whole_tray_count].pack_tray.append(
                                        Item(lying_items_name, 'cube', [tray_length, tray_width, tray_height + lying_items_height],
                                             lying_items_weight+tray_weight, address=picture_address, is_lying=True,
                                             is_mixed=True, pack_item=placed_items, pack_item_number=[placed_item_number]))
                                    self.packer[0].items[whole_tray_count].update_by_pack()
                            whole_tray_count -= 1
                        else:
                            print(f"横放放不下")
                            break
                    else:  # 两个整托对应一个横放
                        if whole_tray_count >= 2:
                            if not whole_tray_flag_list[whole_tray_count] and not whole_tray_flag_list[whole_tray_count-2]:
                                lying_items_name, item_list, lying_items_height, lying_items_weight, picture_address, placed_item_number, placed_items = (
                                    pack_circles(tray_width, lying_box_height_list[whole_tray_count-2] - tray_height, tray_length,
                                                 item_list, self.task_id, whole_tray_count-2, lying_limit=lying_limit))
                                whole_tray_flag_list[whole_tray_count] = True
                                whole_tray_flag_list[whole_tray_count-2] = True
                                # 如果装入
                                if lying_items_height:
                                    self.packer[0].items[whole_tray_count-2].pack_tray.append(
                                        Item(lying_items_name, 'cube', [tray_length, tray_width, tray_height + lying_items_height],
                                             lying_items_weight+tray_weight, address=picture_address, is_lying=True,
                                             is_mixed=True, pack_item=placed_items, pack_item_number=[placed_item_number]))
                                    self.packer[0].items[whole_tray_count-2].update_by_pack()
                            whole_tray_count -= 1
                        else:
                            print(f"横放放不下")
                            break
            else:  # 横放的货物不可以混装
                print("不允许混装的横放计算")
                while item_list:
                    if item_list[residue_item_count].height <= tray_length:  # 一个整托对应一个横放
                        if whole_tray_count >= 0:
                            if not whole_tray_flag_list[whole_tray_count]:
                                lying_items_name, item_list, lying_items_height, lying_items_weight, picture_address, placed_item_number, placed_items = (
                                    pack_circles(tray_width, lying_box_height_list[whole_tray_count] - tray_height, tray_length,
                                                 item_list, self.task_id, whole_tray_count, lying_limit=lying_limit, mix_flag=False))
                                whole_tray_flag_list[whole_tray_count] = True
                                # 如果装入
                                if lying_items_height:
                                    self.packer[0].items[whole_tray_count].pack_tray.append(
                                        Item(lying_items_name, 'cube',
                                             [tray_length, tray_width, tray_height + lying_items_height],
                                             lying_items_weight+tray_weight, address=picture_address, is_lying=True,
                                             pack_item=[placed_items[0]], pack_item_number=[placed_item_number]))
                                    self.packer[0].items[whole_tray_count].update_by_pack()
                            whole_tray_count -= 1
                        else:
                            print(f"横放放不下")
                            break
                    else:  # 两个整托对应一个横放
                        if whole_tray_count >= 2:
                            if not whole_tray_flag_list[whole_tray_count] and not whole_tray_flag_list[whole_tray_count - 2]:
                                lying_items_name, item_list, lying_items_height, lying_items_weight, picture_address, placed_item_number, placed_items = (
                                    pack_circles(tray_width, lying_box_height_list[whole_tray_count - 2] - tray_height, tray_length,
                                                 item_list, self.task_id, whole_tray_count - 2, lying_limit=lying_limit, mix_flag=False))
                                whole_tray_flag_list[whole_tray_count] = True
                                whole_tray_flag_list[whole_tray_count - 2] = True
                                # 如果装入
                                if lying_items_height:
                                    self.packer[0].items[whole_tray_count - 2].pack_tray.append(
                                        Item(lying_items_name, 'cube',
                                             [tray_length, tray_width, tray_height + lying_items_height],
                                             lying_items_weight+tray_weight, address=picture_address, is_lying=True,
                                             pack_item=[placed_items[0]], pack_item_number=[placed_item_number]))
                                    self.packer[0].items[whole_tray_count - 2].update_by_pack()
                            whole_tray_count -= 1
                        else:
                            print(f"横放放不下")
                            break
        self.packer[0].unfit_items = item_list
        return 0

    def print_packed_items_info(self, bin_load_number_list, element_color, bin_v_count, print_info, residue_item_info):
        for i in range(len(self.packer[0].bins)):
            for j in range(len(self.packer[0].bins[i].items)):
                # self.packer[0].bins[i].items[j].pack_tray = list_sort(self.packer[0].bins[i].items[j].pack_tray)
                self.packer[0].bins[i].items[j].pack_tray.sort(key=return_height0, reverse=True)
                self.packer[0].bins[i].items[j].partno = list2name(self.packer[0].bins[i].items[j].pack_tray)
            # self.packer[0].bins[i].items.sort(key=return_height, reverse=True)

        # self.packer[0].packed_items.sort(key=return_height, reverse=True)
        position_count = 0
        whole_tray_count = 0

        # 标色（适用于main中显示）
        for i in range(len(self.packer[0].bins)):
            if self.packer[0].bins[i].items:
                now_tray = self.packer[0].bins[i].items[0]
            for j in range(len(self.packer[0].bins[i].items)):
                temp_item = self.packer[0].bins[i].items[j]
                if now_tray.partno == temp_item.partno:
                    temp_item.color = now_tray.color
                else:
                    whole_tray_count += 1
                    temp_item.color = element_color[whole_tray_count % 20]
                    now_tray = copy.deepcopy(temp_item)

                if position_count % bin_load_number_list[i] == 0:
                    print(' ')
                    print('集装箱' + str(position_count // bin_load_number_list[i] + 1) + ':')

                print('位置' + str(position_count % bin_load_number_list[i] + 1) + ': ' +
                      temp_item.partno + ' 总高度为' + str(temp_item.height))
                position_count += 1

        # 输出文字信息
        for i in range(len(self.packer[0].bins)):
            v_count = 0
            weight_count = 0
            bin_v = self.packer[0].bins[i].length/100*self.packer[0].bins[i].width/100*self.packer[0].bins[i].height/100
            for j in range(len(self.packer[i+1].bins[0].items)):
                temp_item = self.packer[i+1].bins[0].items[j]
                v_count += (temp_item.length/100)*(temp_item.width/100)*(temp_item.height/100)
                weight_count += temp_item.weight
                for k in self.packer[i+1].bins[0].items[j].pack_tray:
                    self.packer[i+1].bins[0].item_number += sum_list(k.pack_item_number)
            information = f'车厢{i+1}货物总体积为{round(v_count, 2)}立方\n空间利用率为{round(v_count / bin_v * 100, 1)}%\n'
            print_info[i] += information
            information = f'总重量为{round(weight_count, 1)}吨\n'
            print_info[i] += information
            print(print_info[i])

        # 输出unfit_items内容
        residue_item_info = item_list2partno(self.packer[0].unfit_items)
        residue_item_number = len(self.packer[0].unfit_items)
        return self.packer, print_info, residue_item_info, residue_item_number


class PackAll:
    def item_to_tray(self, data, task_id, common_size_data, tray_data):
        #
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定使用的中文字体
        plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号
        packer = [Packer()]
        packer_count = 0
        fig = []
        unfit_item_list = []
        unfit_item_number = []
        mixed_count = 0
        items_number_in_a_tray_r = []
        items_number_in_a_tray_n = []

        # 获取货物数据
        foam_height = data['config']['froth_height'] * 10  # mm
        item_name = [item['name'] for item in data['tableData']]
        item_diameter = [item['diameter'] for item in data['tableData']]
        item_height = [int(item['width']) + foam_height for item in data['tableData']]
        item_weight = [item['weight'] for item in data['tableData']]
        item_num = [item['number'] for item in data['tableData']]
        item_level = [item['priority'] for item in data['tableData']]
        item_name_hd = [str(item['order_thickness']) for item in data['tableData']]
        item_hd = [str(item['real_thickness']) for item in data['tableData']]
        item_kd = [str(item['width']) for item in data['tableData']]
        item_name_cd = [str(item['order_height']) for item in data['tableData']]
        item_cd = [str(item['real_height']) for item in data['tableData']]

        # 其他数据处理
        if data['config']['mix']:
            mixed_flag = True
        else:
            mixed_flag = False
        tray_length = tray_data['data']['palletLength'] * 100
        tray_extra_length = data['config']['beyond_height']
        tray_width = tray_data['data']['palletWidth'] * 100
        tray_extra_width = data['config']['beyond_width']
        tray_height = tray_data['data']['palletHeight'] * 100
        tray_weight = tray_data['data']['palletWeight']

        often_thickness = [item['rollThickness'] for item in common_size_data['data']]
        often_length = [item['rollLength'] for item in common_size_data['data']]
        often_number = [item['rollNums'] for item in common_size_data['data']]
        tray = Tray(name="tray", lwh=[tray_length, tray_width, tray_height], extra_length=tray_extra_length,
                    extra_width=tray_extra_width, weight=tray_weight, color="yellow")
        element_color = [
            '#FF0000', '#00FF00', '#0000FF', '#808080', '#FF00FF',
            '#00FFFF', '#800000', '#008000', '#000080', '#808000',
            '#800080', '#008080', '#C0C0C0', '#808080', '#A52A2A',
            '#FFA500', '#800000', '#FF4500', '#2E8B57', '#7B68EE'
        ]

        # 添加货物和进行同规格货物装载，对应要改变的变量为装箱任务、总体积、装箱任务数、托盘、三个用于混装的变量、py中图像显示相关变量
        add_item_instance = AddItemToPackerAndPackSame(packer, packer_count, tray,
                                                       unfit_item_list,
                                                       unfit_item_number,
                                                       items_number_in_a_tray_r,
                                                       items_number_in_a_tray_n, fig)
        result = \
            add_item_instance.add_item_and_pack_same(item_name, item_name_hd, item_hd, item_kd, item_name_cd,
                                                     item_cd, item_diameter, item_height,
                                                     item_weight, item_num, item_level, often_thickness,
                                                     often_length, often_number,
                                                     element_color, mixed_flag, tray_weight, task_id, 0, 1)
        return json.dumps(result, ensure_ascii=False)

    def pack_all(self, data, task_id, truck_size_data, second_input, tray_data, show_flag=False):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定使用的中文字体
        plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号
        start_time = time.time()
        print_info = []
        residue_item_info = ' '
        packer = [Packer()]
        packer_count = 0
        fig = []
        unfit_item_list = []
        unfit_item_number = []
        mixed_count = 0
        items_number_in_a_tray_r = []
        items_number_in_a_tray_n = []

        element_color = [
            '#FF0000', '#00FF00', '#0000FF', '#808080', '#FF00FF',
            '#00FFFF', '#800000', '#008000', '#000080', '#808000',
            '#800080', '#008080', '#C0C0C0', '#808080', '#A52A2A',
            '#FFA500', '#800000', '#FF4500', '#2E8B57', '#7B68EE'
        ]
        bin_count = 0

        print("数据输入")
        bin_id = [item['box_id'] for item in data['config']['box_list']]
        bin_name = []
        bin_length = []
        bin_width = []
        bin_height = []
        bin_max_weight = []
        bin_number = [item['num'] for item in data['config']['box_list']]
        # 对照id 补全输入数据，未做 未找到处理
        for i in range(len(bin_id)):
            for j in range(len(truck_size_data['data'])):
                if bin_id[i] == truck_size_data['data'][j]['id']:
                    bin_name.append(truck_size_data['data'][j]['name'])
                    bin_length.append(truck_size_data['data'][j]['lengthM'] * 100)
                    bin_width.append(truck_size_data['data'][j]['widthM'] * 100)
                    bin_height.append(truck_size_data['data'][j]['heightM'] * 100)
                    bin_max_weight.append(truck_size_data['data'][j]['weightT'])
                    break

        #
        foam_height = data['config']['froth_height'] * 10  # mm
        item_name = [item['name'] for item in data['tableData']]
        item_diameter = [item['diameter'] for item in data['tableData']]
        item_height = [int(item['width']) + foam_height for item in data['tableData']]
        item_weight = [item['weight'] for item in data['tableData']]
        item_num = [item['number'] for item in data['tableData']]
        item_level = [item['priority'] for item in data['tableData']]
        item_name_hd = [str(item['order_thickness']) for item in data['tableData']]
        item_hd = [str(item['real_thickness']) for item in data['tableData']]
        item_kd = [str(item['width']) for item in data['tableData']]
        item_name_cd = [str(item['order_height']) for item in data['tableData']]
        item_cd = [str(item['real_height']) for item in data['tableData']]

        if data['config']['mix']:
            mixed_flag = True
        else:
            mixed_flag = False
        tray_length = int(tray_data['data']['palletLength'] * 100)
        tray_extra_length = data['config']['beyond_height']
        tray_width = int(tray_data['data']['palletWidth'] * 100)
        tray_extra_width = data['config']['beyond_width']
        tray_height = int(tray_data['data']['palletHeight'] * 100)
        tray_weight = tray_data['data']['palletWeight']
        rule = data['config']['rule']
        overlap_flag, overlap_height, overlap_total_height = parse_overlap_limits_cm(data['config'])
        lying_flag = data['config']['lying']
        lying_limit = int(data['config']['lying_limit'])
        lying_tray_flag = data['config']['lying_tray_flag']
        lying_order_limit = data['config']['parmX']

        tray = Tray(name="tray", lwh=[tray_length, tray_width, tray_height], extra_length=tray_extra_length,
                    extra_width=tray_extra_width, weight=tray_weight, color="yellow")
        max_whole_tray_number = 0
        bin_v_count = 0
        bin_load_weight_list = []
        bin_load_number_list = []

        # 添加箱体
        AddBinToPacker_Instance = AddBinToPacker(packer, bin_count, bin_v_count, max_whole_tray_number, fig)
        [packer, bin_count, bin_v_count, max_whole_tray_number, fig, bin_load_weight_list,
         bin_load_number_list, packer_count, print_info] = \
            AddBinToPacker_Instance.add_bin_to_packer(bin_name, bin_number, bin_length, bin_width, bin_height,
                                                      bin_max_weight, tray_length, tray_width, print_info)
        print("添加箱体成功")

        # 添加货物和进行同规格货物装载，对应要改变的变量为装箱任务、总体积、装箱任务数、托盘、三个用于混装的变量、py中图像显示相关变量
        AddItemToPackerAndPackSame_Instance = AddItemToPackerAndPackSame(packer, packer_count, tray,
                                                                         unfit_item_list,
                                                                         unfit_item_number,
                                                                         items_number_in_a_tray_r,
                                                                         items_number_in_a_tray_n, fig)
        [packer, packer_count, unfit_item_list, unfit_item_number, items_number_in_a_tray_r,
         items_number_in_a_tray_n, fig] = \
            AddItemToPackerAndPackSame_Instance.add_item_and_pack_same(item_name, item_name_hd, item_hd, item_kd, item_name_cd, item_cd,
                                                                       item_diameter, item_height,
                                                                       item_weight, item_num, item_level,
                                                                       0, 0, 0,
                                                                       element_color, mixed_flag, tray_weight, task_id,
                                                                       1, bin_count, second_input)
        print("添加货物和进行同规格货物装载成功")

        # 输入需要混装的货物信息，计算混装货物的位置信息
        if mixed_flag:

            print("需要散装的货物有", len(packer[0].unfit_items), "个")
            # 按照同规格货物摆法来摆放不同规格货物（仅限同半径）
            PackerHandler_Instance = PackerHandler(packer, packer_count, unfit_item_list, unfit_item_number,
                                                   mixed_count, fig)
            [packer, packer_count, unfit_item_list, unfit_item_number, mixed_count, fig] = \
                PackerHandler_Instance.mixed_items_pack_as_same(items_number_in_a_tray_r, items_number_in_a_tray_n,
                                                                tray, foam_height, task_id)
            # packer_count += 1
            # 剩下的混装货物使用遗传算法
            unfit_height = []
            unfit_radius = []
            for item in unfit_item_list:
                unfit_height.append(item.height)
                unfit_radius.append(item.length / 2)
            Different_specifications_Instance = DifferentSpecifications(np.array(unfit_height), np.array(unfit_radius),
                                                                        np.array(unfit_item_number),
                                                                        tray.length, tray.width,
                                                                        0.01)
            print('遗传算法计算')
            print(unfit_height)
            print(unfit_radius)
            print(unfit_item_number)
            Different_specifications_Instance.run()
            Different_specifications_result = Different_specifications_Instance.get_res()
            # print(Different_specifications_result)

            # 上一步的结果进一步处理，散装托盘加入packer0
            MixedPacker_Instance = MixedPacker(packer, tray, packer_count, fig)
            [packer, packer_count, fig] = MixedPacker_Instance.pack_mixed_items(Different_specifications_result,
                                                                                foam_height, mixed_count, tray_weight,
                                                                                task_id)

        # 膜叠膜处理
        OverlapHandler_Instance = OverlapHandler(packer)
        packer = OverlapHandler_Instance.handle_overlap(tray_length, tray_width, tray_height, tray_weight,
                                                        overlap_height, overlap_total_height, overlap_flag, foam_height)

        # # 分类处理与贪心处理成整托
        # TrayToWholeTray_Instance = TrayToWholeTray(packer, tray)
        # packer = TrayToWholeTray_Instance.tray2whole(bin_height, element_color)

        # 超出整托个数则进行优化
        OptimizePacking_Instance = OptimizePacking(packer, bin_length, bin_width, bin_height, bin_number, tray,
                                                   max_whole_tray_number, LOADING_RULE, task_id)
        packer = OptimizePacking_Instance.optimize_packing(tray, rule, bin_load_weight_list, bin_load_number_list,
                                                           overlap_flag, tray_height, tray_weight, lying_flag,
                                                           lying_order_limit)

        # 将unfit_items小托信息整理为item_list,进行横放计算
        OptimizePacking_Instance.pack_lying_items(lying_flag, lying_limit, tray_data, mixed_flag, lying_tray_flag)

        # 整托内部排序、标色与文字输出
        packer, print_info, residue_item_info, residue_item_number = \
            OptimizePacking_Instance.print_packed_items_info(bin_load_number_list, element_color, bin_v_count,
                                                             print_info, residue_item_info)

        for i in range(bin_count):
            p = Painter(packer[0].bins[i])
            fig[i] = p.plotBoxAndItems(title=packer[0].bins[i].partno, alpha=0.9, write_num=False, fontsize=10,
                                       plotbox=1)
            if p.patch_zu:
                fig[i].legend(handles=p.patch_zu, labels=p.label_zu)

        end_time = time.time()
        print("用时", round(end_time - start_time, 2), "s")

        if show_flag:
            plt.show()
        return packer, max_whole_tray_number, print_info, residue_item_info, residue_item_number


# 横放算法（二维，将圆装进箱，有重力、层数、支撑限制）
def pack_circles(bin_width, bin_height, other_bin_height, lying_items_list, task_id, whole_tray_count, lying_limit = 4, mix_flag = True):
    """
    将圆形货物放置到指定的箱体中，并移除已放置的货物。

    :param bin_width: 箱体的宽度
    :param bin_height: 箱体的高度
    :param lying_items_list: 待放置的货物列表，每个元素是包含 length 和 partno 属性的对象
    :return: 一个元组，包括已放置的圆形货物名称列表、更新后的未放置货物列表、使用的高度
    """
    bin = Bin2d(bin_width, bin_height)
    # 使用 item.length / 2 作为圆的半径，ID 为 idx+1
    circles = [MyCircle(item.length / 2, idx + 1, weight=item.weight, partno=item.partno, cylinder_length=item.height) for idx, item in enumerate(lying_items_list)]
    # 按半径从大到小排序
    circles.sort(key=lambda c: c.radius, reverse=True)

    total_weight = 0

    if not circles:
        print("lying_items_list 是空的，没有货物需要放置。")
        return [], lying_items_list, 0, 0, "", 0, []

    # 放置第一个圆
    cir_count = 0
    first_flag = False
    for cir_count in range(len(circles)):
        first_circle = circles[cir_count]
        first_circle.set_position(first_circle.radius, first_circle.radius)
        max_height = first_circle.radius * 2
        total_weight = first_circle.weight
        if bin.is_within_bin(first_circle) and not bin.check_overlap(first_circle):
            first_circle.layer = 1
            bin.placed_circles.append(first_circle)
            first_flag = True
            break

    if first_flag:
        # 放置其余的圆形货物
        for circle in circles[cir_count+1:]:
            placed = bin.place_circle(circle, lying_limit=lying_limit)
            if placed and (mix_flag or circle.partno == first_circle.partno):
                # place_circle成功不会自动append，需要手动添加
                bin.placed_circles.append(circle)
                if circle.y + circle.radius > max_height:
                    max_height = circle.y + circle.radius
                total_weight += circle.weight
    else:
        print(f"整托位置{whole_tray_count}横放一个也放不进去")
        return [], lying_items_list, 0, 0, "", 0, []

    # 根据已放置货物的 ID，从 lying_items_list 中移除对应的货物
    # circle.id 对应 lying_items_list 的索引为 circle.id - 1
    placed_item_number = len(bin.placed_circles)
    placed_indices = [c.id - 1 for c in bin.placed_circles]
    updated_lying_items_list = [r for idx, r in enumerate(lying_items_list) if idx not in placed_indices]
    placed_items = [r for idx, r in enumerate(lying_items_list) if idx in placed_indices]

    # 统计已放置货物的partno
    if bin.placed_circles:
        placed_items_name = item_list2partno(bin.placed_circles)
    else:
        return [], lying_items_list, 0, 0, "", 0, []

    # 绘制图片并保存
    address = draw_horizontal_image(bin.placed_circles, bin_width, bin_height, other_bin_height, task_id, whole_tray_count)

    return placed_items_name, updated_lying_items_list, max_height, total_weight, address, placed_item_number, placed_items


def draw_horizontal_image(placed_circles: List[MyCircle], bin_width: float, bin_height: float, other_bin_height: float,
                          order_id: str, name: str = ''):
    """
    可视化装箱结果并保存为图片文件，利用 GridSpec 控制两个子图横向绘图区的物理长度一致。

    :param placed_circles: 已放置的圆形货物列表
    :param bin_width: 箱体的宽度（x 轴范围）
    :param bin_height: 正视图箱体的高度
    :param other_bin_height: 俯视图箱体的高度/长度
    :param order_id: 订单 ID，用于构建保存路径
    :param name: 图片名称
    """
    # 创建 figure，设置合适的尺寸
    fig = plt.figure(figsize=(9, 12))
    # 使用 GridSpec 设置左右边距，保证所有子图的横向显示区域一致
    gs = gridspec.GridSpec(2, 1, left=0.15, right=0.85, hspace=0.3)

    # 分别创建两个子图，第二个子图共享第一个子图的 x 轴
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)

    # 构建保存路径
    base_path = os.path.dirname(os.path.abspath(__file__))
    save_directory = os.path.join(get_static_images_dir(), str(order_id))
    os.makedirs(save_directory, exist_ok=True)

    # 设置正视图（子图1）
    ax1.set_xlim(0, bin_width)
    ax1.set_ylim(0, bin_height)
    ax1.set_aspect('auto')  # 如需 1:1 单位比例，可修改为 'equal'
    ax1.set_xlabel(f'宽 {round(bin_width, 1)}')
    ax1.set_ylabel(f'高 {round(bin_height, 1)}')
    ax1.set_title('横放货物正视图')

    # 设置俯视图（子图2）
    ax2.set_xlim(0, bin_width)
    ax2.set_ylim(0, other_bin_height)
    ax2.set_aspect('auto')  # 如需 1:1 单位比例，可修改为 'equal'
    ax2.set_xlabel(f'宽 {round(bin_width, 1)}')
    ax2.set_ylabel(f'长 {round(other_bin_height, 1)}')
    ax2.set_title('横放货物俯视图')

    # 绘制装箱边界
    rect1 = Rectangle((0, 0), bin_width, bin_height, linewidth=1, edgecolor='black', facecolor='none')
    ax1.add_patch(rect1)

    rect2 = Rectangle((0, 0), bin_width, other_bin_height, linewidth=1, edgecolor='black', facecolor='none')
    ax2.add_patch(rect2)

    # 绘制正视图中的圆形货物
    for circle in placed_circles:
        if circle.is_position_set():
            circ = Circle((circle.x, circle.y), circle.radius, edgecolor='blue', facecolor='cyan', alpha=0.5)
            ax1.add_patch(circ)
            ax1.text(circle.x, circle.y, f"{circle.partno}", horizontalalignment='center',
                     verticalalignment='center', fontsize=8, color='black')
        else:
            print(f"圆形货物 {circle.id} 未被放置")

    # 绘制俯视图（用矩形表示圆柱正投影）
    for circle in placed_circles:
        if circle.is_position_set():
            rect = Rectangle((circle.x - circle.radius, 0), circle.radius * 2, circle.cylinder_length,
                             edgecolor='blue', facecolor='cyan', alpha=1)
            ax2.add_patch(rect)
            # 如果需要标注编号，可取消下面注释
            # ax2.text(circle.x, circle.cylinder_length / 2, f"{circle.partno}",
            #          horizontalalignment='center', verticalalignment='center', fontsize=8, color='black')
        else:
            print(f"圆形货物 {circle.id} 未被放置")

    # 构建完整的保存文件路径
    full_save_path = os.path.join(save_directory, f"{name}.png")
    relative_path = build_asset_path('images', order_id, f'{name}.png')

    # 保存图像，dpi 可根据需要调整
    plt.savefig(full_save_path, bbox_inches='tight', dpi=150)
    plt.clf()
    plt.close(fig)

    print(f"装箱可视化图片已保存到: {full_save_path}")
    return relative_path


def item_list2partno(item_list):
    if not item_list:
        return ""
    # 统计已放置货物的partno
    item_partno = item_list[0].partno
    item_count = 1
    placed_items_name = ''
    for item in item_list[1:]:
        if item.partno != item_partno:
            if placed_items_name:
                placed_items_name += "+"
            placed_items_name += f"{item_partno}*{item_count}"
            item_partno = item.partno
            item_count = 1
        else:
            item_count += 1
    if placed_items_name:
        placed_items_name += "+"
    placed_items_name += f"{item_partno}*{item_count}"
    return placed_items_name


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定使用的中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号
    with open('test1.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    with open('common_size_data.json', 'r', encoding='utf-8') as file:
        json_common_size_data = json.load(file)
    with open('second_data.json', 'r', encoding='utf-8') as file:
        json_second_data = json.load(file)
    print(json_data)
    PackAll_Instance = PackAll()
    result_1 =\
        PackAll_Instance.item_to_tray(data=json_data["data"], common_size_data=json_common_size_data, task_id=json_data["task_id"])
    print(result_1)

    p, whole_tray_number, info, residue_item_info = \
        PackAll_Instance.pack_all(json_second_data["sourceJson"], json_second_data["taskId"], json_common_size_data, json_second_data["middleJsonObj"], show_flag=True)
    print(info)
    print(residue_item_info)
