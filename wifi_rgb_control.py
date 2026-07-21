from mpython import *
import socket
import time
import network

# ============ WiFi连接配置 ============
WIFI_SSID = 'haoda7'
WIFI_PASSWORD = '0123456789'

# ============ 当前RGB状态 ============
current_r = 0
current_g = 0
current_b = 0
is_on = False

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
    ip_addr = my_wifi.sta.ifconfig()[0]
    oled.fill(0)
    oled.DispChar('WiFi已连接', 16, 0, 1)
    oled.DispChar('IP:', 0, 16, 1)
    oled.DispChar(ip_addr, 24, 16, 1)
    oled.DispChar('手机浏览器访问', 0, 32, 1)
    oled.DispChar('当前:' + get_color_name(), 0, 48, 1)
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

# ============ 连接WiFi ============
oled.fill(0)
oled.DispChar('正在连接WiFi...', 8, 16, 1)
oled.show()

my_wifi = wifi()
my_wifi.connectWiFi(WIFI_SSID, WIFI_PASSWORD)

while not my_wifi.sta.isconnected():
    time.sleep_ms(500)

ip = my_wifi.sta.ifconfig()[0]
print("WiFi Connected! IP: " + ip)

# ============ 创建Web服务器(非阻塞模式) ============
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)
s.setblocking(False)  # 关键:非阻塞模式,不卡住主循环

show_status()

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
        html += "<p class='st'>状态: 开 (" + str(current_r) + "," + str(current_g) + "," + str(current_b) + ")</p>"
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
    html += "<div class='sec'><div class='sec-t'>-- 亮度 --</div>"
    for lv in [255, 180, 100, 30]:
        html += "<a class='br' style='background:#16213e' href='/?r=" + str(lv) + "," + str(lv) + "," + str(lv) + "'>" + str(lv) + "</a>"
    html += "</div>"
    html += "</body></html>"
    return html

def parse_query(request):
    q_start = request.find('?')
    if q_start == -1:
        return None
    space = request.find(' ', q_start)
    if space == -1:
        return None
    query = request[q_start + 1:space]
    if 'off=1' in query:
        return 'off'
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
    return (r, g, b)

# ============ 本地按键控制 ============
def on_button_a_down(_):
    time.sleep_ms(10)
    if button_a.value() == 1:
        return
    show_status()

def on_button_b_down(_):
    time.sleep_ms(10)
    if button_b.value() == 1:
        return
    if is_on:
        set_rgb(0, 0, 0, on=False)
    else:
        set_rgb(255, 255, 255, on=True)

button_a.irq(trigger=Pin.IRQ_FALLING, handler=on_button_a_down)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=on_button_b_down)

# ============ 主循环(非阻塞轮询) ============
last_web_check = time.ticks_ms()

while True:
    try:
        current_time = time.ticks_ms()

        # 每500ms检查一次web请求(关键:不能一直阻塞在accept上)
        if time.ticks_diff(current_time, last_web_check) > 500:
            last_web_check = current_time
            try:
                client, addr = s.accept()
                client.settimeout(2)
                request = client.recv(1024).decode('utf-8')

                result = parse_query(request)

                if result == 'off':
                    set_rgb(0, 0, 0, on=False)
                    print("RGB OFF")
                elif result is not None:
                    set_rgb(result[0], result[1], result[2], on=True)
                    print("RGB: (" + str(current_r) + "," + str(current_g) + "," + str(current_b) + ")")

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
