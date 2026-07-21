from mpython import *
import time
from machine import Timer

return_to_menu = False

def show_main_menu():
    oled.fill(0)
    oled.DispChar('RGB呼吸灯效果', 20, 0, 1)
    oled.DispChar('A键:单色呼吸', 0, 16, 1)
    oled.DispChar('B键:彩虹呼吸', 0, 32, 1)
    oled.DispChar('触摸Y:多彩呼吸', 0, 48, 1)
    oled.DispChar('触摸P:返回菜单', 0, 60, 1)
    oled.show()

def breath_single_color():
    global return_to_menu
    breath = 0
    while not return_to_menu:
        while breath <= 255 and not return_to_menu:
            rgb.fill((int(breath), int(0), int(0)))
            rgb.write()
            time.sleep_ms(5)
            breath += 1
        while breath >= 0 and not return_to_menu:
            rgb.fill((int(breath), int(0), int(0)))
            rgb.write()
            time.sleep_ms(5)
            breath -= 1

def breath_rainbow():
    global return_to_menu
    r, g, b = 255, 0, 0
    while not return_to_menu:
        while g < 255 and r == 255 and not return_to_menu:
            g += 1
            rgb.fill((int(r), int(g), int(b)))
            rgb.write()
            time.sleep_ms(5)
        while r > 0 and g == 255 and not return_to_menu:
            r -= 1
            rgb.fill((int(r), int(g), int(b)))
            rgb.write()
            time.sleep_ms(5)
        while b < 255 and r == 0 and not return_to_menu:
            b += 1
            rgb.fill((int(r), int(g), int(b)))
            rgb.write()
            time.sleep_ms(5)
        while g > 0 and b == 255 and not return_to_menu:
            g -= 1
            rgb.fill((int(r), int(g), int(b)))
            rgb.write()
            time.sleep_ms(5)
        while r < 255 and g == 0 and not return_to_menu:
            r += 1
            rgb.fill((int(r), int(g), int(b)))
            rgb.write()
            time.sleep_ms(5)
        while b > 0 and r == 255 and not return_to_menu:
            b -= 1
            rgb.fill((int(r), int(g), int(b)))
            rgb.write()
            time.sleep_ms(5)

def breath_colorful():
    global return_to_menu
    red_breath = 0
    green_breath = 0
    blue_breath = 0
    while not return_to_menu:
        while red_breath <= 255 and not return_to_menu:
            while green_breath <= 255 and not return_to_menu:
                while blue_breath <= 255 and not return_to_menu:
                    rgb.fill((int(red_breath), int(green_breath), int(blue_breath)))
                    rgb.write()
                    time.sleep_ms(2)
                    blue_breath += 1
                green_breath += 1
            red_breath += 1
        while red_breath >= 0 and not return_to_menu:
            while green_breath >= 0 and not return_to_menu:
                while blue_breath >= 0 and not return_to_menu:
                    rgb.fill((int(red_breath), int(green_breath), int(blue_breath)))
                    rgb.write()
                    time.sleep_ms(2)
                    blue_breath -= 1
                green_breath -= 1
            red_breath -= 1

_status_p = 0
_status_y = 0

def on_touchpad_P_pressed():
    global _status_p, return_to_menu
    _status_p = 1
    return_to_menu = True

def on_touchpad_Y_pressed():
    global _status_y
    _status_y = 1

tim12 = Timer(12)
def timer12_tick(_):
    global _status_p, _status_y
    try:
        if touchPad_P.read() < 400:
            if 1 != _status_p:
                _status_p = 1
                on_touchpad_P_pressed()
        elif 0 != _status_p:
            _status_p = 0
        if touchPad_Y.read() < 400:
            if 1 != _status_y:
                _status_y = 1
                on_touchpad_Y_pressed()
        elif 0 != _status_y:
            _status_y = 0
    except:
        pass
tim12.init(period=100, mode=Timer.PERIODIC, callback=timer12_tick)

def on_button_a_down(_):
    global return_to_menu
    time.sleep_ms(10)
    if button_a.value() == 1:
        return
    return_to_menu = False
    oled.fill(0)
    oled.DispChar('单色呼吸灯', 25, 20, 1)
    oled.DispChar('触摸P返回', 25, 36, 1)
    oled.show()
    breath_single_color()
    rgb.fill((0, 0, 0))
    rgb.write()
    show_main_menu()

def on_button_b_down(_):
    global return_to_menu
    time.sleep_ms(10)
    if button_b.value() == 1:
        return
    return_to_menu = False
    oled.fill(0)
    oled.DispChar('彩虹呼吸灯', 25, 20, 1)
    oled.DispChar('触摸P返回', 25, 36, 1)
    oled.show()
    breath_rainbow()
    rgb.fill((0, 0, 0))
    rgb.write()
    show_main_menu()

button_a.irq(trigger=Pin.IRQ_FALLING, handler=on_button_a_down)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=on_button_b_down)

show_main_menu()

while True:
    if _status_y == 1:
        _status_y = 0
        return_to_menu = False
        oled.fill(0)
        oled.DispChar('多彩呼吸灯', 25, 20, 1)
        oled.DispChar('触摸P返回', 25, 36, 1)
        oled.show()
        breath_colorful()
        rgb.fill((0, 0, 0))
        rgb.write()
        show_main_menu()