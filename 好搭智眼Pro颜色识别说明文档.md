# 好搭智眼Pro颜色识别OLED显示与RGB联动 — 项目说明

## 一、项目简介

本项目运行于 **掌控板（mPython）**，通过 I2C 连接 **好搭智眼Pro** 视觉识别模块，实时识别摄像头画面中指定区域的颜色，将识别结果（RGB分量、颜色ID、颜色中文名）显示在掌控板 OLED 屏幕上，并同步驱动板载 3 颗 RGB 灯显示对应颜色。

- **硬件平台**：掌控板（ESP32）+ 好搭智眼Pro（K210 视觉模块）
- **开发环境**：MicroPython + `mpython` 库 + `haodaAIPro` 库
- **文件名**：`haoda_aieye_color_oled.py`

## 二、硬件资源

| 资源 | 说明 |
| --- | --- |
| 好搭智眼Pro | 通过 I2C 与掌控板通信，需先加载 `haodaAIPro` 扩展库 |
| OLED 显示屏 | 128×64，单行高度 16px，共 4 行有效显示区 |
| 板载 RGB 灯 ×3 | 通过 `rgb.fill((r,g,b))` + `rgb.write()` 同步驱动 |

## 三、好搭智眼Pro 颜色识别 API

> ⚠️ Pro 版与普通版（好搭智眼）API 完全不同，不可混用。

### 1. 关键 API 对照

| 步骤 | Pro 版（本项目使用） | 普通版（不可混用） |
| --- | --- | --- |
| 导入 | `from haodaAIPro import *` | `from haodaAI import *` |
| 实例化 | `hl = HaodaAIPro(i2c)` | `hl = haodaAI(i2c)` |
| 等待就绪 | `hl.waitDeviceReadyOk()` | 无 |
| 切换算法 | `hl.VisionBegin(ai_algorithm_e.kColorRecognizer)` | `hl.set_algorithm_cr()` |
| 设置区域数 | `hl.setParamNum(n)` | `hl.set_param_Num(n)` |
| 设置区域参数 | `hl.setParamColor(i, x, y, w, h)` | `hl.set_param_Color(i, x, y, w, h)` |
| 获取结果 | `hl.getRaw()` 返回 list 或 `None` | `hl.getResult()` + `hl.getID()` |
| 字段访问 | `hl_result[i].result_data1~5` | `hl.get(i, haodaai_obj_info_e.kLabel)` |

### 2. 颜色识别结果字段映射

| 字段 | 含义 |
| --- | --- |
| `result_data1` | R 红色分量 |
| `result_data2` | G 绿色分量 |
| `result_data3` | B 蓝色分量 |
| `result_data5` | 颜色标签 ID |

### 3. 颜色标签 ID 对照表

| ID | 颜色 | RGB 灯颜色 |
| --- | --- | --- |
| 1 | 黑色 | `(0, 0, 0)` |
| 2 | 白色 | `(255, 255, 255)` |
| 3 | 红色 | `(255, 0, 0)` |
| 4 | 绿色 | `(0, 255, 0)` |
| 5 | 蓝色 | `(0, 0, 255)` |
| 6 | 黄色 | `(255, 255, 0)` |
| 其它 | 未知颜色 | `(0, 0, 0)` 灯灭 |

> Pro 官方文档说明颜色识别共支持 7 种颜色标签，但范例代码与公开枚举中仅能确认上述 6 种。第 7 种若需补充，可在掌控板 REPL 中执行：`from haodaAIPro import *; print([x for x in dir(color_label_e) if x.startswith('kColor')])` 查询。

## 四、OLED 显示布局（4 行）

```
好搭智眼Pro颜色识别        <- y=0   标题
R:xxx G:xxx B:xxx          <- y=16  RGB原始分量
颜色ID：x                   <- y=32  颜色标签ID
颜色：红色                  <- y=48  颜色中文名
```

## 五、核心设计

### 1. 初始化流程

```python
hl = HaodaAIPro(i2c)                       # 实例化
hl.waitDeviceReadyOk()                     # 等待摄像头上电就绪
hl.VisionBegin(ai_algorithm_e.kColorRecognizer)  # 启动颜色识别算法
hl.setParamNum(4)                          # 设置4个识别区域
hl.setParamColor(0, 380, 180, 80, 120)     # 配置区域0：(x, y, w, h)
```

### 2. 颜色表设计

颜色表采用 `(中文名, RGB灯颜色)` 元组结构，一次查表同时取得显示文本与灯色：

```python
颜色表 = {
    1: ('黑色', (0, 0, 0)),
    2: ('白色', (255, 255, 255)),
    # ...
}
颜色名, rgb_color = 颜色表.get(颜色ID, ('未知颜色', (0, 0, 0)))
```

### 3. 主循环（轮询刷新）

- 通过 `hl.getRaw()` 获取识别结果（可能返回 `None`，需判空）
- 每次成功识别后同步刷新 OLED 与 RGB 灯
- 循环周期 100ms，平衡刷新率与 CPU 占用

## 六、使用方法

1. **硬件连接**：用专用 4P 连接线将好搭智眼Pro 接到掌控板 I2C 接口
2. **加载扩展库**：在好搭Block 中按 `添加扩展 → 好搭智眼Pro` 加载 `haodaAIPro` 库到掌控板
3. **上传程序**：通过 mPython / Mu / Thonny 将 `haoda_aieye_color_oled.py` 上传到掌控板
4. **运行观察**：
   - OLED 显示"等待摄像头上电中" → "摄像头启动完成"
   - 将带颜色的物体置于摄像头视野内的识别区域
   - OLED 显示颜色信息，RGB 灯同步亮起对应颜色

## 七、参考文档

- 好搭智眼Pro 官方学习手册：https://www.yuque.com/hhdd/aieye
- 颜色识别算法详解：https://www.yuque.com/hhdd/aieye/qwmzu2z35iai5ew9
- 官方扩展库添加说明：https://www.yuque.com/hhdd/aieye/iqob2s3nuy38mt2s
- Pro 版范例代码来源：`extracted_code3.txt` 第 1409-1452 行（`03-好搭智眼Pro-颜色识别.hd`）

## 八、可扩展方向

- 启用 4 个识别区域（当前仅使用区域0），在 OLED 上分块显示
- 增加颜色置信度判断，过滤低置信度结果避免抖动
- 通过 WiFi 将识别结果上报到物联网平台
- 联动语音合成模块播报颜色名称
- 结合色块识别算法 (`kFindBlobs`) 实现目标颜色追踪
