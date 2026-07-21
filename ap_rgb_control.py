from mpython import *
import socket
import time
import network

# ============ AP热点配置 ============
AP_SSID = 'haoda_ctrl'      # 热点名称(英文,手机可见)
AP_PASSWORD = '0123456789'  # 至少8位

# ============ 当前RGB状态 ============
current_r = 0
current_g = 0
current_b = 0
is_on = False
# 基础颜色(满亮度下的颜色,亮度调节基于此缩放)
base_r = 255
base_g = 255
base_b = 255
brightness = 255  # 当前亮度0-255

# ============ 初始化RGB灯 ============
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
    oled.DispChar('热点:' + AP_SSID, 0, 0, 1)
    oled.DispChar('密码:' + AP_PASSWORD, 0, 16, 1)
    oled.DispChar('IP:192.168.4.1', 0, 32, 1)
    oled.DispChar('当前:' + get_color_name(), 0, 48, 1)
    oled.show()

def set_color(r, g, b, on=True):
    """设置颜色,同时更新基础颜色和亮度=255"""
    global current_r, current_g, current_b, is_on, base_r, base_g, base_b, brightness
    current_r = r
    current_g = g
    current_b = b
    base_r = r
    base_g = g
    base_b = b
    brightness = 255
    is_on = on
    if on:
        rgb.fill((int(r), int(g), int(b)))
    else:
        rgb.fill((0, 0, 0))
    rgb.write()
    show_status()

def set_brightness(lv):
    """根据亮度缩放当前基础颜色"""
    global current_r, current_g, current_b, brightness, is_on
    brightness = lv
    is_on = True
    # 按比例缩放,四舍五入
    current_r = (base_r * lv + 127) // 255
    current_g = (base_g * lv + 127) // 255
    current_b = (base_b * lv + 127) // 255
    rgb.fill((int(current_r), int(current_g), int(current_b)))
    rgb.write()
    show_status()

# 保留旧函数名兼容(本文件未使用,但避免外部调用出错)
def set_rgb(r, g, b, on=True):
    set_color(r, g, b, on)

# ============ 创建AP热点 ============
oled.fill(0)
oled.DispChar('正在创建热点...', 8, 16, 1)
oled.show()

# 先关闭STA模式,再开启AP模式
sta_if = network.WLAN(network.STA_IF)
if sta_if.active():
    sta_if.active(False)

ap_if = network.WLAN(network.AP_IF)
ap_if.active(True)
# authmode: 0=OPEN, 2=WPA-PSK, 3=WPA2-PSK, 4=WPA/WPA2-PSK
ap_if.config(essid=AP_SSID, authmode=network.AUTH_WPA2_PSK, password=AP_PASSWORD)

# 等待AP启动
for _ in range(20):
    if ap_if.active():
        break
    time.sleep_ms(100)

# ESP32 AP模式默认IP为192.168.4.1
ip = ap_if.ifconfig()[0]
print("AP Started! SSID=%s, IP=%s" % (AP_SSID, ip))

show_status()

# ============ 创建Web服务器(非阻塞模式) ============
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)
s.setblocking(False)  # 关键:非阻塞模式

# ============ HTML控制页面 ============
def get_html():
    html = "<!DOCTYPE html>"
    html += "<html><head><meta charset='UTF-8'>"
    html += "<meta name='viewport' content='width=device-width,initial-scale=1'>"
    html += "<title>RGB控制</title>"
    html += "<style>"
    html += "*{margin:0;padding:0;box-sizing:border-box}"
    html += "body{font-family:Arial,sans-serif;background:#1a1a2e;color:#fff;padding:15px;text-align:center}"
    html += "h1{font-size:20px;margin-bottom:12px;color:#e94560}"
    html += ".st{font-size:13px;color:#888;margin-bottom:12px}"
    html += ".sec{margin-bottom:15px}"
    html += ".sec-t{font-size:14px;color:#aaa;margin-bottom:8px}"
    html += ".cb{display:inline-block;width:55px;height:55px;border-radius:12px;border:3px solid #333;margin:4px;cursor:pointer}"
    html += ".cb.on{border-color:#fff}"
    html += ".br{display:block;width:100%;padding:14px;font-size:16px;font-weight:bold;border:none;border-radius:10px;cursor:pointer;margin:5px 0;color:#fff;text-decoration:none}"
    html += ".off{background:#c0392b}"
    html += ".wht{background:#27ae60}"
    html += "</style></head><body>"
    html += "<h1>掌控板RGB灯</h1>"
    if is_on:
        pct = brightness * 100 // 255
        html += "<p class='st'>颜色: (" + str(base_r) + "," + str(base_g) + "," + str(base_b) + ") 亮度: " + str(pct) + "%</p>"
    else:
        html += "<p class='st'>状态: 关</p>"
    html += "<div class='sec'><div class='sec-t'>-- 颜色 --</div>"
    colors = [
        ("#e74c3c", "255,0,0"),
        ("#2ecc71", "0,255,0"),
        ("#3498db", "0,0,255"),
        ("#f1c40f", "255,255,0"),
        ("#e91e63", "255,0,128"),
        ("#00bcd4", "0,255,255"),
        ("#ff9800", "255,153,0"),
        ("#9c27b0", "128,0,255"),
        ("#ffffff", "255,255,255")
    ]
    for c in colors:
        border = " on" if is_on and (str(current_r) + "," + str(current_g) + "," + str(current_b)) == c[1] else ""
        html += "<a class='cb" + border + "' style='background:" + c[0] + "' href='/?r=" + c[1] + "'></a>"
    html += "</div>"
    html += "<div class='sec'>"
    html += "<a class='br off' href='/?off=1'>关灯</a>"
    html += "<a class='br wht' href='/?r=255,255,255'>开灯(白)</a>"
    html += "</div>"
    html += "<div class='sec'><div class='sec-t'>-- 亮度 (基于当前颜色) --</div>"
    for lv in [255, 180, 100, 30]:
        pct = lv * 100 // 255
        # 按钮背景色随当前基础颜色变化,直观显示
        br_r = (base_r * lv + 127) // 255
        br_g = (base_g * lv + 127) // 255
        br_b = (base_b * lv + 127) // 255
        bg = "rgb(%d,%d,%d)" % (br_r, br_g, br_b)
        border = " border:3px solid #fff;" if brightness == lv else ""
        html += "<a class='br' style='background:" + bg + border + "' href='/?b=" + str(lv) + "'>" + str(pct) + "%</a>"
    html += "</div>"
    html += "</body></html>"
    return html

def parse_query(request):
    """解析URL参数,返回('off',)、(r,g,b)、('b', lv) 或 None"""
    q_start = request.find('?')
    if q_start == -1:
        return None
    space = request.find(' ', q_start)
    if space == -1:
        return None
    query = request[q_start + 1:space]
    if 'off=1' in query:
        return ('off',)
    # 亮度调节 b=亮度值
    b_start = query.find('b=')
    if b_start != -1:
        b_str = query[b_start + 2:].split('&')[0].split(' ')[0]
        try:
            return ('b', int(b_str))
        except:
            return None
    # 颜色 r=r,g,b
    val_start = query.find('r=')
    if val_start == -1:
        return None
    val_str = query[val_start + 2:]
    comma1 = val_str.find(',')
    if comma1 == -1:
        return None
    r = int(val_str[:comma1])
    rest = val_str[comma1 + 1:]
    comma2 = rest.find(',')
    if comma2 == -1:
        return None
    g = int(rest[:comma2])
    b = int(rest[comma2 + 1:])
    return ('rgb', r, g, b)

# ============ 本地按键控制 ============
color_list = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 255),
]
color_index = 0

def on_button_a_down(_):
    global color_index
    time.sleep_ms(10)
    if button_a.value() == 1:
        return
    color_index = (color_index + 1) % len(color_list)
    c = color_list[color_index]
    set_color(c[0], c[1], c[2])

def on_button_b_down(_):
    time.sleep_ms(10)
    if button_b.value() == 1:
        return
    if is_on:
        set_color(0, 0, 0, on=False)
    else:
        c = color_list[color_index]
        set_color(c[0], c[1], c[2])

button_a.irq(trigger=Pin.IRQ_FALLING, handler=on_button_a_down)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=on_button_b_down)

# ============ 主循环(非阻塞轮询) ============
last_web_check = time.ticks_ms()

while True:
    try:
        current_time = time.ticks_ms()

        # 每500ms检查一次web请求
        if time.ticks_diff(current_time, last_web_check) > 500:
            last_web_check = current_time
            try:
                client, addr = s.accept()
                client.settimeout(2)
                request = client.recv(1024).decode('utf-8')

                result = parse_query(request)

                if result is None:
                    pass
                elif result[0] == 'off':
                    set_color(0, 0, 0, on=False)
                    print("RGB OFF")
                elif result[0] == 'rgb':
                    set_color(result[1], result[2], result[3], on=True)
                    print("RGB: (" + str(current_r) + "," + str(current_g) + "," + str(current_b) + ")")
                elif result[0] == 'b':
                    set_brightness(result[1])
                    print("Brightness: " + str(result[1]) + " -> (" + str(current_r) + "," + str(current_g) + "," + str(current_b) + ")")

                html = get_html()
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nConnection: close\r\n\r\n" + html
                client.send(response.encode('utf-8'))
                client.close()

            except OSError:
                pass  # 无连接时静默跳过

    except Exception as e:
        print("Error: " + str(e))
        time.sleep(1)

    time.sleep_ms(10)  # 关键:让出CPU给WiFi底层
