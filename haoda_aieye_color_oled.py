from mpython import *
from haodaAI import *
import time

# 颜色ID -> 中文名映射（来自好搭智眼Pro颜色识别算法）
颜色表 = {
    1: '黑色',
    2: '白色',
    3: '红色',
    4: '绿色',
    5: '蓝色',
    6: '黄色',
}

# 初始化好搭智眼Pro
hl = haodaAI(i2c)

def waiting_handler(_event):
    """等待算法切换完成，并在OLED上提示状态"""
    while not _event:
        oled.fill_rect(0, 0, 128, 16, 0)
        oled.DispChar('好搭智眼正在切换算法...', 0, 0, 1)
        oled.show()
        time.sleep(0.5)
    oled.fill_rect(0, 0, 128, 16, 0)
    if _event == 1:
        oled.DispChar('好搭智眼切换算法成功', 0, 0, 1)
        oled.show()
        time.sleep(1)
        oled.fill_rect(0, 0, 128, 16, 0)
    elif _event == -1:
        oled.DispChar('好搭智眼不支持此算法', 0, 0, 1)
        oled.show()
    else:
        oled.fill_rect(0, 16, 128, 32, 0)
        oled.DispChar('未检测到好搭智眼', 0, 0, 1)
        oled.DispChar('请检查连接状态', 0, 16, 1)
        oled.DispChar('确认连接后按RST按键', 0, 32, 1)
        oled.show()

# 启动提示
oled.fill(0)
oled.DispChar('好搭智眼颜色识别', 16, 0, 1)
oled.DispChar('正在初始化...', 16, 32, 1)
oled.show()

# 切换到颜色识别算法
waiting_handler(hl.set_algorithm_cr())

# 主循环：识别颜色并显示在OLED
while True:
    if hl.getResult() > 0:
        ID = hl.getID()
        颜色名 = 颜色表.get(ID, '未知')
        oled.fill(0)
        oled.DispChar('好搭智眼颜色识别', 16, 0, 1)
        oled.DispChar(str('ID：') + str(ID), 0, 24, 1)
        oled.DispChar(str('颜色：') + str(颜色名), 0, 40, 1)
        oled.show()
    time.sleep_ms(200)
