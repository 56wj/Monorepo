import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import os


def plot_result_diff(ax , box_width , box_length , result_x , r):
    n_num = int(len(result_x) / 2)
    coordinate_x = result_x[:n_num]
    coordinate_y = result_x[n_num:]
    # 绘制正方形
    square = patches.Rectangle((0, 0), box_length, box_width, linewidth=1, edgecolor='b', facecolor='none')
    ax.add_patch(square)

    plt.xlim(0, box_length)
    plt.ylim(0, box_width)

    # 绘制圆形
    for i in range(n_num):
        circle_x, circle_y, circle_radius = coordinate_x[i], coordinate_y[i], r[i]
        circle_patch = plt.Circle((circle_x, circle_y), circle_radius, fill=False, color='r')
        ax.add_patch(circle_patch)

    # 设置坐标轴纵横比例为相等，保证正方形和圆形按比例绘制
    ax.set_aspect('equal', 'box')

    # 隐藏坐标轴的下标
    ax.set_xticks([])
    ax.set_yticks([])


item_data = 0 #  pd.read_excel('测试数据.xlsx', sheet_name="货物信息")
bin_data = 0 #  pd.read_excel('测试数据.xlsx', sheet_name="集装箱信息")
tray_data = 0 #  pd.read_excel('测试数据.xlsx', sheet_name="托盘与其他")
number_data = 0 #  pd.read_excel('测试数据.xlsx', sheet_name="常用规格")


def init(address):
    global item_data, bin_data, tray_data, number_data
    item_data = pd.read_excel(address, sheet_name="货物信息")
    bin_data = pd.read_excel(address, sheet_name="集装箱信息")
    tray_data = pd.read_excel(address, sheet_name="托盘与其他")
    number_data = pd.read_excel(address, sheet_name="常用规格")
    return 0


def get_name():
    return np.array(item_data['品名'])


def get_hd():
    hd = np.array(item_data['订单厚度']).astype(str)
    return hd


def get_kd():
    kd = np.array(item_data['宽度']).astype(str)
    return kd


def get_cd():
    cd = np.array(item_data['订单长度']).astype(str)
    return cd


# 单位:mm
def get_direct():
    return np.array(item_data['直径'], dtype=float)


# 单位:mm
def get_height():
    return np.array(item_data['宽度'], dtype=float)


# 单位:ton
def get_weight():
    return np.array(item_data['订单重量'], dtype=float)


def get_number():
    return np.array(item_data['订单卷数'], dtype=float)


def get_bin_name():
    return np.array(bin_data['名称'])


def get_bin_length():
    return np.array(bin_data['长(m)'])


def get_bin_width():
    return np.array(bin_data['宽(m)'])


def get_bin_height():
    return np.array(bin_data['高(m)'])


def get_bin_number():
    return np.array(bin_data['数量'])


def get_tray_length():
    return np.array(tray_data['托盘长度(m)'][0])


def get_tray_extra_length():
    return np.array(tray_data['允许超出长度的范围(m)'][0])


def get_tray_width():
    return np.array(tray_data['托盘宽度(m)'][0])


def get_tray_extra_width():
    return np.array(tray_data['允许超出宽度的范围(m)'][0])


def get_tray_height():
    return np.array(tray_data['托盘高度(m)'][0])


def get_tray_weight():
    return np.array(tray_data['托盘重量(t)'][0])


def get_mixed():
    return np.array(tray_data['是否允许混装'][0])


def get_overlap():
    if np.array(tray_data['是否支持膜叠膜'][0]) == '是':
        return True
    else:
        return False


def get_overlap_height():
    return np.array(tray_data['单个膜叠膜货物高度限制（cm）'][0])


def get_overlap_total_height():
    return np.array(tray_data['膜叠膜货物总高度限制（cm）'][0])


def get_foam_height():
    return np.array(tray_data['泡沫垫高度(cm)'][0])


def get_often_thickness():
    return np.array(number_data['膜卷厚度'])


def get_often_length():
    return np.array(number_data['膜卷长度'])


def get_often_number14():
    return np.array(number_data['1.4*1.1托盘'])


def get_often_number13():
    return np.array(number_data['1.3*1.1托盘'])


def get_often_number11():
    return np.array(number_data['1.1*1.1托盘'])
