from scipy.optimize import basinhopping
import numpy as np
import matplotlib.pyplot as plt
import time
import Tool


class DifferentSpecifications:
    def __init__(self, height, r, n_num, box_width, box_length, target_fitness):
        self.height = height
        self.n_num = n_num
        self.r = r
        self.box_width = box_width
        self.box_length = box_length
        self.target_fitness = target_fitness

        self.temp_num = 0

        self.global_result = []
        self.global_radius = []
        self.temp_res = []

        h_idx = np.argsort(height)
        self.height = height[h_idx]
        self.r = r[h_idx]
        self.n_num = n_num[h_idx]

        '''将数据放入list中'''
        self.category = []
        self.radius = []

        for idx, item in enumerate(self.n_num):
            num = self.n_num[idx]
            for i in range(num):
                self.radius.append(self.r[idx])
                self.category.append(idx)

    def callback(self, x, f, accept):
        # iteration_history.append(f)
        if f < self.target_fitness:
            return True  # 满足停止条件，返回True停止优化
        return False

    def func(self, x):
        total = 0
        coordinate_x = x[:self.temp_num]
        coordinate_y = x[self.temp_num:]
        for i in range(self.temp_num):
            if coordinate_x[i] - self.temp_res[i] < 0:
                total -= coordinate_x[i] - self.temp_res[i]
            if coordinate_x[i] + self.temp_res[i] > self.box_length:
                total += (coordinate_x[i] + self.temp_res[i] - self.box_length)
            if coordinate_y[i] - self.temp_res[i] < 0:
                total -= coordinate_y[i] - self.temp_res[i]
            if coordinate_y[i] + self.temp_res[i] > self.box_width:
                total += coordinate_y[i] + self.temp_res[i] - self.box_width
        for i in range(self.temp_num):
            for j in range(i + 1, self.temp_num):
                if np.sqrt((coordinate_x[j] - coordinate_x[i]) ** 2 + (coordinate_y[j] - coordinate_y[i]) ** 2) < \
                        self.temp_res[i] + self.temp_res[j]:
                    total += (self.temp_res[i] + self.temp_res[j] - np.sqrt(
                        (coordinate_x[j] - coordinate_x[i]) ** 2 + (coordinate_y[j] - coordinate_y[i]) ** 2)) * 2
        return total

    def run(self):
        best_result = 0
        while len(self.radius) != 0:
            self.temp_res.append(self.radius.pop())
            self.temp_num = len(self.temp_res)
            x0 = [self.box_length / 2] * self.temp_num + [self.box_width / 2] * self.temp_num
            result = basinhopping(self.func, x0=x0, minimizer_kwargs={
                "bounds": [(0, self.box_length)] * self.temp_num + [(0, self.box_width)] * self.temp_num},
                                  callback=self.callback,
                                  niter=self.temp_num * 10, stepsize=0.1)
            if result.fun < self.target_fitness:
                # print(f'放入货物为{self.temp_res}，已找到结果')
                best_result = result
            else:
                # print(f'放入货物为{self.temp_num}，未找到结果')
                self.global_result.append(best_result)
                self.radius.append(self.temp_res.pop())
                self.global_radius.append(self.temp_res)
                self.temp_res = []

        '''将最终一轮放入结果中'''
        if len(self.temp_res) != 0:
            self.global_result.append(best_result)
            self.global_radius.append(self.temp_res)

    def plot_result(self):
        num_plots = len(self.global_result)
        fig, axs = plt.subplots(num_plots, figsize=(6, 4 * num_plots))
        if num_plots != 1:
            for idx, (result_item, radius_item) in enumerate(zip(self.global_result, self.global_radius)):
                Tool.plot_result_diff(axs[idx], self.box_width, self.box_length, result_item.x, radius_item)
            plt.show()
        else:
            for idx, (result_item, radius_item) in enumerate(zip(self.global_result, self.global_radius)):
                Tool.plot_result_diff(axs, self.box_width, self.box_length, result_item.x, radius_item)
            plt.show()

    def get_res(self):
        res = []
        # print(self.global_result[0].x)
        for (result_item, radius_item) in zip(self.global_result, self.global_radius):
            temp_res = []
            temp_res.append(result_item.x[:int(len(result_item.x) / 2)])
            temp_res.append(result_item.x[int(len(result_item.x) / 2):])
            temp_res.append(radius_item)
            res.append(temp_res)
        return res


if __name__ == '__main__':
    # 高度
    height = np.array([4, 3, 2])
    # 半径
    r = np.array([0.23, 0.13, 0.17])
    # 数量
    n_num = np.array([3, 3, 1])
    # 箱体参数
    box_width = 1
    box_length = 1
    # fit阈值
    target_fitness = 0.01
    s = DifferentSpecifications(height, r, n_num, box_width, box_length, target_fitness)
    s.run()
    re = s.get_res()
    print(re)
    s.plot_result()


# [[array([0.80384229, 0.52535105, 0.1852673 , 0.37137942, 0.76845119,0.31009791]),
#   array([0.21507749, 0.41118383, 0.38833869, 0.14740656, 0.72905911,0.76843069]),
#   [0.17, 0.17, 0.17, 0.13, 0.23, 0.23]],
#  [array([0.5]), array([0.5]), [0.23]]]