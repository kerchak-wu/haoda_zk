from mpython import *
from mpython_ble.application import BLEUART
import time

# ============ 当前RGB状态 ============
current_r = 0
current_g = 0
current_b = 0
is_on = False
ble_connected = False

# ============ 初始化RGB灯(关) ============
rgb.fill((0, 0, 0))
rgb.write()

def get_color_name():
    if not is_on:
        return '关'
    if current_r == 255 and current_g == 0 and current_b == 0:
        return '红'
    if current_r == 0 and current_g == 255 and current_b == 0:
        return '绿'
    if current_r == 0 and current_g == 0 and current_b == 255:
        return '蓝'
    if current_r == 255 and current_g == 255 and current_b == 0:
        return '黄'
    if current_r == 0 and current_g == 255 and current_b == 255:
        return '青'
    if current_r == 255 and current_g == 0 and current_b == 255:
        return '洋红'
    if current_r == 255 and current_g == 255 and current_b == 255:
        return '白'
    return '自定义'

def show_status():
    oled.fill(0)
    if ble_connected:
        oled.DispChar('蓝牙已连接', 16, 0, 1)
    else:
        oled.DispChar('蓝牙:RGB_CTRL', 8, 0, 1)
        oled.DispChar('等待手机连接...', 0, 16, 1)
    oled.DispChar('当前:' + get_color_name(), 0, 32, 1)
    oled.DispChar('R%d G%d B%d' % (current_r, current_g, current_b), 0, 48, 1)
    oled.show()

def set_rgb(r, g, b, on=True):
    global current_r, current_g, current_b, is_on
    current_r = r
    current_g = g
    current_b = b
    is_on = on
    if on:
        rgb.fill((int(r), int(g), int(b)))
    else:
        rgb.fill((0, 0, 0))
    rgb.write()
    show_status()

def process_command(cmd):
    """处理手机发来的指令"""
    cmd = cmd.strip().upper()
    if not cmd:
        return

    # 单字符指令
    if cmd == 'R':
        set_rgb(255, 0, 0)
    elif cmd == 'G':
        set_rgb(0, 255, 0)
    elif cmd == 'B':
        set_rgb(0, 0, 255)
    elif cmd == 'Y':
        set_rgb(255, 255, 0)
    elif cmd == 'C':
        set_rgb(0, 255, 255)
    elif cmd == 'M':
        set_rgb(255, 0, 255)
    elif cmd == 'W':
        set_rgb(255, 255, 255)
    elif cmd in ('O', '0', 'OFF'):
        set_rgb(0, 0, 0, on=False)
    # 三元组指令 r,g,b
    elif ',' in cmd:
        try:
            parts = cmd.split(',')
            if len(parts) >= 3:
                r = max(0, min(255, int(parts[0])))
                g = max(0, min(255, int(parts[1])))
                b = max(0, min(255, int(parts[2])))
                set_rgb(r, g, b)
        except:
            pass

# ============ 蓝牙接收回调 ============
def ble_uart_irq():
    global ble_connected
    try:
        received = bytes(_ble_uart.read()).decode('UTF-8', 'ignore')
        process_command(received)
        # 回显当前状态给手机
        if _ble_uart.is_connected():
            _ble_uart.write(bytes('OK %s R%dG%dB%d\n' % (
                get_color_name(), current_r, current_g, current_b), 'utf-8'))
    except:
        pass

# ============ 创建蓝牙BLE串口 ============
_ble_uart = BLEUART(name=bytes('RGB_CTRL', 'utf-8'))
_ble_uart.irq(handler=ble_uart_irq)

show_status()

# ============ 本地按键控制 ============
color_list = [
    (255, 0, 0),     # 红
    (0, 255, 0),     # 绿
    (0, 0, 255),     # 蓝
    (255, 255, 0),   # 黄
    (0, 255, 255),   # 青
    (255, 0, 255),   # 洋红
    (255, 255, 255), # 白
]
color_index = 0

def on_button_a_down(_):
    """A键:切换颜色"""
    global color_index
    time.sleep_ms(10)
    if button_a.value() == 1:
        return
    color_index = (color_index + 1) % len(color_list)
    c = color_list[color_index]
    set_rgb(c[0], c[1], c[2])

def on_button_b_down(_):
    """B键:开关灯"""
    time.sleep_ms(10)
    if button_b.value() == 1:
        return
    if is_on:
        set_rgb(0, 0, 0, on=False)
    else:
        c = color_list[color_index]
        set_rgb(c[0], c[1], c[2])

button_a.irq(trigger=Pin.IRQ_FALLING, handler=on_button_a_down)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=on_button_b_down)

# ============ 主循环(检查连接状态) ============
last_check = 0

while True:
    # 每500ms更新一次连接状态
    if time.ticks_diff(time.ticks_ms(), last_check) > 500:
        last_check = time.ticks_ms()
        try:
            connected = _ble_uart.is_connected()
            if connected != ble_connected:
                ble_connected = connected
                show_status()
        except:
            pass

    time.sleep_ms(50)
