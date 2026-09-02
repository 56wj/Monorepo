import os
from flask import Flask, send_from_directory
import requests
from main import PackAll, generator_excel
import json
import warnings
from matplotlib import pyplot as plt
from suspend_algo import SuspendPack
from rectpack import newPacker, MaxRectsBl, GuillotineBlsfSas, MaxRectsBlsf, MaxRectsBaf, MaxRectsBssf, MaxRectsBbef, MaxRectsBiof
from path_utils import get_static_images_dir, build_asset_path
app = Flask(__name__)
element_color = ['#87ceeb', '#98ff98', '#fffacd', '#ffc0cb', '#d3d3d3', '#f46d43', '#74add1', '#fdae61', '#abd9e9']

# 假设你的图片存放在 static/images 文件夹下
IMAGES_FOLDER = get_static_images_dir()

# 设置字体（SimHei 是一个常用的支持中文的字体，可以替换为你系统中的其他字体）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

api_base_url = os.getenv('INTERNAL_API_BASE_URL', 'http://localhost:8101').rstrip('/')

PALLET_ROLL_SPEC_URL = f"{api_base_url}/specification/palletroll/queryByPalletId"
TRUCK_SPEC_URL = f"{api_base_url}/specification/truck/queryAll"
PALLET_SPEC_URL = f"{api_base_url}/specification/pallet/queryById"
TUBE_SPEC_URL = f"{api_base_url}/specification/tube/queryAll"

def task_to_run1(receive_data):
    try:
        request_data = receive_data.get('data')
        print(request_data)
        task_id = receive_data.get('task_id')
        tray_id = request_data.get('config')
        tray_id = tray_id.get('tray_size')
        # 打印接收到的请求消息
        print("接收第一次数据成功")
        common_size_data = 0

        #  获取托盘规格
        print(f"获取托盘规格")
        tray_id_params = {'palletId': tray_id}
        response = requests.get(PALLET_SPEC_URL, params=tray_id_params, timeout=(3, 30))
        # 检查响应状态码
        if response.status_code == 200:
            # 如果响应状态码为 200，表示请求成功
            tray_data = response.json()  # 解析 JSON 格式的响应数据
            print(tray_data)
        else:
            raise RuntimeError(f"pallet specification request failed: {response.status_code}")

        # 获取规格表
        print("获取规格表")
        response = requests.get(PALLET_ROLL_SPEC_URL, params=tray_id_params, timeout=(3, 30))
        # 检查响应状态码
        if response.status_code == 200:
            # 如果响应状态码为 200，表示请求成功
            common_size_data = response.json()  # 解析 JSON 格式的响应数据
            print(common_size_data)
        else:
            raise RuntimeError(f"pallet-roll specification request failed: {response.status_code}")

        print('开始计算')
        PackAll_Instance = PackAll()
        result = PackAll_Instance.item_to_tray(request_data, task_id, common_size_data, tray_data)
        print(type(result))
        output = {"result": result, "taskId": task_id}
        return output
    except Exception as e:
        print(str(e))
        raise


def task_to_run2(receive_data):
    try:
        # receive_data = request.get_json()
        request_data = receive_data.get('sourceJson')
        tray_id = request_data.get('config')
        tray_id = tray_id.get('tray_size')
        n_in_tray_data = receive_data.get('middleJsonObj')
        task_id = receive_data.get('taskId')
        orderid = request_data["config"]["orderId"]
        common_size_data = 0
        # 打印接收到的请求消息
        # print("Received Request Data:", request_data)
        print("接收第二次数据成功")

        # 获取车厢规格表
        response = requests.get(TRUCK_SPEC_URL, timeout=(3, 30))
        # 检查响应状态码
        if response.status_code == 200:
            # 如果响应状态码为 200，表示请求成功
            truck_size_data = response.json()  # 解析 JSON 格式的响应数据
            # print(common_size_data)
            print("获取规格表成功")
        else:
            # 如果请求失败，打印错误信息
            print("Failed to retrieve data. Status code:", response.status_code)
            raise RuntimeError(f"truck specification request failed: {response.status_code}")

        #  获取托盘规格
        print(f"获取托盘规格")
        tray_id_params = {'palletId': tray_id}
        response = requests.get(PALLET_SPEC_URL, params=tray_id_params, timeout=(3, 30))
        # 检查响应状态码
        if response.status_code == 200:
            # 如果响应状态码为 200，表示请求成功
            tray_data = response.json()  # 解析 JSON 格式的响应数据
            print(tray_data)
        else:
            raise RuntimeError(f"pallet specification request failed: {response.status_code}")

        print('开始计算')
        PackAll_Instance = PackAll()
        p, whole_tray_number, info, residue_item_info, residue_item_number = \
            PackAll_Instance.pack_all(request_data, task_id, truck_size_data, n_in_tray_data, tray_data)
        print(f"计算完成")
        max_length = []
        a = {}
        b = {}
        color_count = -1
        color_list = ['#FF0000', '#00FF00', '#0000FF', '#FFFFFF', '#FF00FF',
                      '#00FFFF', '#800000', '#008000', '#000080', '#808000',
                      '#800080', '#008080', '#C0C0C0', '#808080', '#A52A2A',
                      '#FFA500', '#800000', '#FF4500', '#2E8B57', '#7B68EE']
        for l in range(len(p[0].bins)):
            max_length.append(0)
            for i in range(len(p[0].bins[l].items)):
                item = p[0].bins[l].items[i]
                # print(len(item.pack_tray_h), max_length)
                if len(item.pack_tray) > max_length[l]:
                    max_length[l] = len(item.pack_tray)
        packed_items_number = 0
        for l in range(len(p[0].bins)):
            tray_count = 0
            left_n = 0
            left_w = 0
            right_n = 0
            right_w = 0
            for j in range(max_length[l]):
                dict_list = []
                color_count += 1
                for i in range(len(p[0].bins[l].items)):
                    item = p[0].bins[l].items[i]
                    if j < len(item.pack_tray):
                        dict_list.append(
                            {'value': [i // 2, i % 2, round(item.pack_tray[j].height, 2)],
                             'name': item.pack_tray[j].partno if not item.pack_tray[j].is_lying else f"横放{item.pack_tray[j].partno}",
                             'address': item.pack_tray[j].address,
                             'itemStyle': {'color': element_color[color_count % len(element_color)] if not item.pack_tray[j].is_lying else "#800080"}})
                        color_list[i % 20] = element_color[color_count % len(element_color)]
                        if not item.pack_tray[j].is_lying or request_data["config"]["lying_tray_flag"]:
                            tray_count += 1
                    else:
                        dict_list.append(
                            {'value': [i // 2, i % 2, 0], 'name': '0', 'itemStyle': {'color': color_list[i % 20]}})
                a[f'data{j+1}'] = dict_list
            a["info"] = info[l]
            a["whole_tray_number"] = p[0].bins[l].max_whole_number
            a["bin_height"] = p[0].bins[l].height
            a["item_number"] = p[0].bins[l].item_number
            a["tray_number"] = tray_count
            packed_items_number += p[0].bins[l].item_number
            a["bin_name"] = p[0].bins[l].partno
            excel_data = {}
            for i in range(p[0].bins[l].max_whole_number):
                if i < len(p[0].bins[l].items):
                    item = p[0].bins[l].items[i]
                    excel_data_thickness = ""
                    excel_data_width = ""
                    excel_data_number = ""
                    excel_data_weight = 0
                    for k in range(len(item.pack_tray)):
                        if not item.pack_tray[k].is_lying:
                            if not item.pack_tray[k].is_mixed:
                                index1 = item.pack_tray[k].pack_item[0].partno.find("*")
                                index2 = item.pack_tray[k].pack_item[0].partno.find("*", index1 + 1)
                                if excel_data_thickness:
                                    excel_data_thickness += "+"
                                excel_data_thickness += item.pack_tray[k].pack_item[0].partno[0:index1]
                                if excel_data_width:
                                    excel_data_width += "+"
                                excel_data_width += item.pack_tray[k].pack_item[0].partno[index1+1:index2]
                                if excel_data_number:
                                    excel_data_number += "+"
                                if item.pack_tray[k].pack_item_number:
                                    excel_data_number += str(item.pack_tray[k].pack_item_number[0])
                                else:
                                    index3 = item.pack_tray[k].partno.find("*", index2 + 1)
                                    excel_data_number += item.pack_tray[k].partno[index3+1:]
                                if i % 2 == 0:
                                    left_n += item.pack_tray[k].pack_item_number[0] if item.pack_tray[k].pack_item_number else int(item.pack_tray[k].partno[index3+1:])
                                else:
                                    right_n += item.pack_tray[k].pack_item_number[0] if item.pack_tray[k].pack_item_number else int(item.pack_tray[k].partno[index3+1:])
                            else:
                                if excel_data_thickness:
                                    excel_data_thickness += "+"
                                excel_data_thickness += "("
                                if excel_data_width:
                                    excel_data_width += "+"
                                excel_data_width += "("
                                if excel_data_number:
                                    excel_data_number += "+"
                                excel_data_number += "("
                                for j in range(len(item.pack_tray[k].pack_item)):
                                    index1 = item.pack_tray[k].pack_item[j].partno.find("*")
                                    index2 = item.pack_tray[k].pack_item[j].partno.find("*", index1 + 1)
                                    if j:
                                        excel_data_thickness += "+"
                                        excel_data_width += "+"
                                        excel_data_number += "+"
                                    excel_data_thickness += item.pack_tray[k].pack_item[j].partno[0:index1]
                                    excel_data_width += item.pack_tray[k].pack_item[j].partno[index1+1:index2]
                                    # 有点疑问，可优化
                                    if item.pack_tray[k].pack_item_number:
                                        excel_data_number += str(item.pack_tray[k].pack_item_number[j])
                                    else:
                                        excel_data_number += "1"
                                if i % 2 == 0:
                                    left_n += item.pack_tray[k].pack_item_number[0] if len(item.pack_tray[k].pack_item_number) == 1 else sum(item.pack_tray[k].pack_item_number)
                                else:
                                    right_n += item.pack_tray[k].pack_item_number[0] if len(item.pack_tray[k].pack_item_number) == 1 else sum(item.pack_tray[k].pack_item_number)
                                excel_data_thickness += ")"
                                excel_data_width += ")"
                                excel_data_number += ")"
                        else:  # 横放货物
                            index1 = item.pack_tray[k].pack_item[0].partno.find("*")
                            index2 = item.pack_tray[k].pack_item[0].partno.find("*", index1 + 1)
                            if excel_data_thickness:
                                excel_data_thickness += "+"
                            excel_data_thickness += item.pack_tray[k].pack_item[0].partno[0:index1]
                            if excel_data_width:
                                excel_data_width += "+"
                            excel_data_width += item.pack_tray[k].pack_item[0].partno[index1 + 1:index2]
                            if excel_data_number:
                                excel_data_number += "+"
                            excel_data_number += f"\"{item.pack_tray[k].pack_item_number[0]}\""
                            if i % 2 == 0:
                                left_n += item.pack_tray[k].pack_item_number[0]
                            else:
                                right_n += item.pack_tray[k].pack_item_number[0]
                        excel_data_weight += item.pack_tray[k].weight
                        if i % 2 == 0:
                            left_w += excel_data_weight
                        else:
                            right_w += excel_data_weight
                    excel_data_tray = {"no": i+1, "thickness": excel_data_thickness, "width": excel_data_width,
                                       "total_width": item.height, "number": excel_data_number,
                                       "weight": round(excel_data_weight, 2)}
                    excel_data[f"tray{i+1}"] = excel_data_tray
                else:
                    excel_data_tray = {"no": i + 1, "thickness": "", "width": "", "total_width": 0, "number": "", "weight": 0}
                    excel_data[f"tray{i + 1}"] = excel_data_tray
            mwn = p[0].bins[l].max_whole_number
            excel_data_tray = {"no": mwn+1, "thickness": "", "width": "", "total_width": 0, "number": left_n,
                               "weight": round(left_w, 2)}
            excel_data[f"tray{mwn + 1}"] = excel_data_tray
            excel_data_tray = {"no": mwn + 2, "thickness": "", "width": "", "total_width": 0, "number": right_n,
                               "weight": round(right_w, 2)}
            excel_data[f"tray{mwn + 2}"] = excel_data_tray
            a["excel_data"] = excel_data
            b[f'bin_item{l+1}'] = a
            a = {}
        b["residue"] = residue_item_info
        b["residue_item_number"] = residue_item_number
        b["all_number"] = packed_items_number + residue_item_number
        excel_address = build_asset_path("images", task_id, f"{orderid}.xlsx")
        b["excel_address"] = excel_address
        excel_address = f"{os.path.dirname(__file__)}/static/images/{task_id}/{orderid}.xlsx"
        generator_excel(b, f"{os.path.dirname(__file__)}/export_template.xlsx", excel_address, orderid, info[0][5:12])
        result_param = json.dumps(b, ensure_ascii=False)
        print(result_param)

        output = {
            'result': result_param,
            'taskId': task_id,
            'resultExcel': b["excel_address"]
        }
        return output
    except Exception as e:
        print(e)
        raise


def select_suspend_result_legacy(results):
    max_result = None
    for result in results:
        if max_result is None:
            max_result = result
        elif result["remain_items_count"] < max_result["remain_items_count"]:
            print(f"legacy选用{result.get('algo_name')}后剩余{result['remain_items_count']}")
            max_result = result
    return max_result


def select_suspend_result(results):
    return min(
        results,
        key=lambda result: (
            result.get("has_enclosed_hole", False),
            result["remain_items_count"],
            result.get("enclosed_hole_area", 0)
        )
    )


def task_to_run3(receive_data):
    request_data = receive_data.get('data')
    # tray_id = request_data.get('config')
    task_id = receive_data.get('taskId')
    arrive_date = request_data["config"]["recDate"]
    print(request_data["config"])
    # orderid = request_data["config"]["orderId"]

    # 获取车厢规格表
    response = requests.get(TRUCK_SPEC_URL, timeout=(3, 30))
    # 检查响应状态码
    if response.status_code == 200:
        # 如果响应状态码为 200，表示请求成功
        truck_size_data = response.json()  # 解析 JSON 格式的响应数据
        # print(common_size_data)
        print("获取规格表成功")
    else:
        # 如果请求失败，打印错误信息
        print("Failed to retrieve data. Status code:", response.status_code)
        raise RuntimeError(f"truck specification request failed: {response.status_code}")

    # 获取纸管规格
    response = requests.get(TUBE_SPEC_URL, timeout=(3, 30))
    # 检查响应状态码
    if response.status_code == 200:
        # 如果响应状态码为 200，表示请求成功
        tube_size_data = response.json()  # 解析 JSON 格式的响应数据
        print("获取规格表成功")
    else:
        # 如果请求失败，打印错误信息
        print("Failed to retrieve data. Status code:", response.status_code)
        raise RuntimeError(f"tube specification request failed: {response.status_code}")

    print('开始计算')
    suspend_pack_instance = SuspendPack(request_data, truck_size_data, task_id, arrive_date, tube_size_data)
    algos = [MaxRectsBlsf, MaxRectsBaf, MaxRectsBssf, MaxRectsBbef, MaxRectsBiof]
    # algos = [MaxRectsBiof]
    candidate_results = []
    for algo in algos:
        result = suspend_pack_instance.pack(algo=algo)
        print(str(algo) + "  :  " + str(result))
        candidate_results.append(result)

    legacy_result = select_suspend_result_legacy(candidate_results)
    if os.getenv("SUSPEND_USE_LEGACY_SELECTOR", "").strip() == "1":
        max_result = legacy_result
        max_result["selection_mode"] = "legacy_remain_items_count"
    else:
        max_result = select_suspend_result(candidate_results)
        max_result["selection_mode"] = "no_enclosed_hole_first"
        max_result["legacy_selected_algo"] = legacy_result.get("algo_name")
        max_result["legacy_has_enclosed_hole"] = legacy_result.get("has_enclosed_hole", False)
        max_result["candidate_layout_checks"] = [
            {
                "algo_name": item.get("algo_name"),
                "remain_items_count": item.get("remain_items_count"),
                "has_enclosed_hole": item.get("has_enclosed_hole", False),
                "enclosed_hole_area": item.get("enclosed_hole_area", 0)
            }
            for item in candidate_results
        ]
    print(
        f"最终选用{max_result.get('algo_name')}, "
        f"剩余{max_result['remain_items_count']}, "
        f"存在空洞: {max_result.get('has_enclosed_hole')}, "
        f"选择模式: {max_result.get('selection_mode')}"
    )
    result = json.dumps(max_result, ensure_ascii=False)
    print(result)
    print(f"计算完成")
    output = {'result': result, 'taskId': task_id}
    return output


@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_FOLDER, filename)

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定使用的中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
