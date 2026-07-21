from mpython import *
from haodaAIPro import *
import time

# 颜色ID -> (中文名, RGB灯颜色)映射（好搭智眼Pro颜色识别算法）
# 1~6 来自Pro官方范例与普通版共用枚举 color_label_e
# 第7种以"未知"兜底，若 REPL 中确认有其他颜色可在此追加
颜色表 = {
    1: ('黑色', (0, 0, 0)),
    2: ('白色', (255, 255, 255)),
    3: ('红色', (255, 0, 0)),
    4: ('绿色', (0, 255, 0)),
    5: ('蓝色', (0, 0, 255)),
    6: ('黄色', (255, 255, 0)),
}

# ============ 初始化OLED提示 ============
oled.fill(0)
oled.DispChar('好搭智眼Pro颜色识别', 0, 0, 1)
oled.DispChar('等待摄像头上电中', 0, 16, 1)
oled.show()

# ============ 初始化好搭智眼Pro ============
# Pro版API与普通版不同：模块名 haodaAIPro，类名 HaodaAIPro
hl = HaodaAIPro(i2c)
hl.waitDeviceReadyOk()                      # Pro特有：等待设备就绪

oled.fill_rect(0, 16, 128, 16, 0)
oled.DispChar('摄像头启动完成', 0, 16, 1)
oled.show()

# ============ 启动颜色识别算法 ============
# Pro版统一通过 VisionBegin + ai_algorithm_e 枚举切换算法
hl.VisionBegin(ai_algorithm_e.kColorRecognizer)

# ============ 设置识别区域 ============
# Pro版必须先设置区域数量与参数（普通版可不设置走默认）
hl.setParamNum(4)                           # 4个识别区域
time.sleep_ms(200)
hl.setParamColor(0, 380, 180, 80, 120)      # 区域0: (x, y, w, h)
time.sleep_ms(50)

# ============ 主循环：识别颜色并显示在OLED ============
while True:
    hl_result = hl.getRaw()                # Pro版通用结果获取
    if hl_result != None:
        R = hl_result[0].result_data1
        G = hl_result[0].result_data2
        B = hl_result[0].result_data3
        颜色ID = hl_result[0].result_data5   # 颜色标签ID
        颜色名, rgb_color = 颜色表.get(颜色ID, ('未知颜色', (0, 0, 0)))

        # 板载RGB灯显示对应颜色
        rgb.fill(rgb_color)
        rgb.write()
        time.sleep_ms(1)

        oled.fill(0)
        oled.DispChar('好搭智眼Pro颜色识别', 0, 0, 1)
        oled.DispChar(str('R:') + str(R) + ' G:' + str(G) + ' B:' + str(B), 0, 16, 1)
        oled.DispChar(str('颜色ID：') + str(颜色ID), 0, 32, 1)
        oled.DispChar(str('颜色：') + str(颜色名), 0, 48, 1)
        oled.show()
    time.sleep_ms(100)
