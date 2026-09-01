# 装箱计算模块说明

## 1. 项目简介
本文档仅说明Python装箱计算模块，包括运行环境、依赖安装、启动方式、核心文件说明。

该模块主要负责装箱优化计算、悬空装箱处理、结果导出等功能，可通过接口方式被上层系统调用。  

## 2. 运行环境
- Python 3.8.10

## 3. 安装依赖
在项目根目录执行：

```bash
pip install -r requirements.txt
```

如遇环境差异问题，可安装完整环境依赖：

```
pip install -r requirements_full.txt
```

## 4. 启动方式

在项目根目录执行：

```
python api_test.py
```

## 5. 核心文件说明

- `api_test.py`：模块接口启动入口，负责接收请求并调用核心算法逻辑
- `main.py`：装箱计算主逻辑
- `suspend_algo.py`：悬空装箱相关算法逻辑
- `Different_specifications.py`：多规格相关处理逻辑
- `auxiliary_methods.py`：辅助计算方法
- `Tool.py`：工具函数
- `rectpack/`：装箱相关算法模块
- `static/`：静态资源目录
- `export_template.xlsx`：结果导出模板文件
