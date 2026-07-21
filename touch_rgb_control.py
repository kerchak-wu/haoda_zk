from mpython import *
import time
from machine import Timer

# ============ 状态变量 ============
current_led = 0          # 当前选中的RGB灯索引(0/1/2)，3表示全部
is_on = False            # 灯是否点亮
color_index = 0          # 当前颜色索引
brightness = 255         # 亮度 0-255（按基础颜色缩放）

# 基础颜色（满亮度值，亮度调节基于此缩放）
color_table = [
    (255, 0, 0),       # 红
    (0, 255, 0),       # 绿
    (0, 0, 255),       # 蓝
    (255, 255, 0),     # 黄
    (0, 255, 255),     # 青
    (255, 0, 255),     # 紫
    (255, 255, 255),   # 白
]
color_names = ['红', '绿', '蓝', '黄', '青', '紫', '白']

# ============ 显示与控制函数 ============
def get_target_name():
    if current_led == 3:
        return '全部'
    return 'LED' + str(current_led + 1)

def get_status_name():
    return '开' if is_on else '关'

def update_display():
    oled.fill(0)
    oled.DispChar('触摸键控制RGB灯', 10, 0, 1)
    oled.DispChar('目标:' + get_target_name() + ' 状态:' + get_status_name(), 0, 16, 1)
    oled.DispChar('颜色:' + color_names[color_index], 0, 32, 1)
    pct = brightness * 100 // 255
    oled.DispChar('亮度:' + str(pct) + '%', 0, 48, 1)
    oled.show()

def apply_led():
    """根据当前状态点亮或熄灭RGB灯"""
    if is_on:
        br = brightness
        base = color_table[color_index]
        color = ((base[0] * br + 127) // 255,
                 (base[1] * br + 127) // 255,
                 (base[2] * br + 127) // 255)
    else:
        color = (0, 0, 0)
    if current_led == 3:
        rgb.fill(color)
    else:
        rgb[current_led] = color
    rgb.write()

# ============ 触摸键处理函数 ============
def on_touchpad_P_pressed():
    """P: 开关灯"""
    global is_on
    is_on = not is_on
    apply_led()
    update_display()

def on_touchpad_Y_pressed():
    """Y: 切换颜色"""
    global color_index
    color_index = (color_index + 1) % len(color_table)
    if is_on:
        apply_led()
    update_display()

def on_touchpad_T_pressed():
    """T: 切换选中的RGB灯（LED1 -> LED2 -> LED3 -> 全部）"""
    global current_led
    current_led = (current_led + 1) % 4
    apply_led()
    update_display()

def on_touchpad_H_pressed():
    """H: 增加亮度（每次+32）"""
    global brightness
    brightness = min(255, brightness + 32)
    apply_led()
    update_display()

def on_touchpad_O_pressed():
    """O: 降低亮度（每次-32）"""
    global brightness
    brightness = max(0, brightness - 32)
    apply_led()
    update_display()

def on_touchpad_N_pressed():
    """N: 全部RGB立即熄灭"""
    global is_on
    is_on = False
    rgb.fill((0, 0, 0))
    rgb.write()
    update_display()

# ============ 触摸键轮询（Timer周期扫描） ============
_status_p = 0
_status_y = 0
_status_t = 0
_status_h = 0
_status_o = 0
_status_n = 0

tim12 = Timer(12)
def timer12_tick(_):
    global _status_p, _status_y, _status_t, _status_h, _status_o, _status_n
    try:
        touchPad_P.read()  # 触发一次读取，避免I2C异常
    except:
        return
    if touchPad_P.read() < 400:
        if _status_p != 1:
            _status_p = 1
            on_touchpad_P_pressed()
    elif _status_p != 0:
        _status_p = 0
    if touchPad_Y.read() < 400:
        if _status_y != 1:
            _status_y = 1
            on_touchpad_Y_pressed()
    elif _status_y != 0:
        _status_y = 0
    if touchPad_T.read() < 400:
        if _status_t != 1:
            _status_t = 1
            on_touchpad_T_pressed()
    elif _status_t != 0:
        _status_t = 0
    if touchPad_H.read() < 400:
        if _status_h != 1:
            _status_h = 1
            on_touchpad_H_pressed()
    elif _status_h != 0:
        _status_h = 0
    if touchPad_O.read() < 400:
        if _status_o != 1:
            _status_o = 1
            on_touchpad_O_pressed()
    elif _status_o != 0:
        _status_o = 0
    if touchPad_N.read() < 400:
        if _status_n != 1:
            _status_n = 1
            on_touchpad_N_pressed()
    elif _status_n != 0:
        _status_n = 0

tim12.init(period=100, mode=Timer.PERIODIC, callback=timer12_tick)

# ============ 初始化 ============
rgb.fill((0, 0, 0))
rgb.write()
update_display()

while True:
    time.sleep_ms(50)
