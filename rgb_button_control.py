from mpython import *
import time
from machine import Timer

# 状态变量
current_led = 0          # 当前选中的RGB灯索引(0/1/2)，3表示全部
is_on = False            # 灯是否点亮
color_index = 0          # 当前颜色索引

# 颜色表（R, G, B）
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

def get_target_name():
    if current_led == 3:
        return '全部'
    return 'LED' + str(current_led + 1)

def get_status_name():
    return '开' if is_on else '关'

def update_display():
    oled.fill(0)
    oled.DispChar('按键控制RGB灯', 20, 0, 1)
    oled.DispChar('目标: ' + get_target_name(), 0, 16, 1)
    oled.DispChar('状态: ' + get_status_name(), 0, 32, 1)
    oled.DispChar('颜色: ' + color_names[color_index], 0, 48, 1)
    oled.DispChar('A切色 B开关 P选灯', 0, 60, 1)
    oled.show()

def apply_led():
    """根据当前状态点亮或熄灭RGB灯"""
    if is_on:
        color = color_table[color_index]
    else:
        color = (0, 0, 0)
    if current_led == 3:
        rgb.fill(color)
    else:
        rgb[current_led] = color
    rgb.write()

def on_button_a_down(_):
    """A键：切换颜色"""
    global color_index
    time.sleep_ms(10)
    if button_a.value() == 1:
        return
    color_index = (color_index + 1) % len(color_table)
    apply_led()
    update_display()

def on_button_b_down(_):
    """B键：开/关灯"""
    global is_on
    time.sleep_ms(10)
    if button_b.value() == 1:
        return
    is_on = not is_on
    apply_led()
    update_display()

button_a.irq(trigger=Pin.IRQ_FALLING, handler=on_button_a_down)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=on_button_b_down)

# 触摸按键P：切换选中的RGB灯（LED1 -> LED2 -> LED3 -> 全部 -> LED1）
_status_p = 0
def on_touchpad_P_pressed():
    global current_led, _status_p
    _status_p = 1
    current_led = (current_led + 1) % 4
    apply_led()
    update_display()

tim12 = Timer(12)
def timer12_tick(_):
    global _status_p
    try:
        if touchPad_P.read() < 400:
            if 1 != _status_p:
                _status_p = 1
                on_touchpad_P_pressed()
        elif 0 != _status_p:
            _status_p = 0
    except:
        pass
tim12.init(period=100, mode=Timer.PERIODIC, callback=timer12_tick)

# 初始化
rgb.fill((0, 0, 0))
rgb.write()
update_display()

while True:
    time.sleep_ms(50)
