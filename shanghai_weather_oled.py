from mpython import *
import network
import time
import json
import urequests
from machine import Timer

# ============ WiFi连接配置 ============
WIFI_SSID = 'haoda7'
WIFI_PASSWORD = '0123456789'

# ============ 心知天气API配置 ============
# 复用项目内已有的API密钥（见 extracted_code.txt 第1431行）
WEATHER_API_KEY = 'S68-rNDesn1uy3ODc'
CITY = 'shanghai'  # 上海
NOW_URL = 'https://api.seniverse.com/v3/weather/now.json?key=' + WEATHER_API_KEY
DAILY_URL = 'https://api.seniverse.com/v3/weather/daily.json?key=' + WEATHER_API_KEY

# ============ 全局天气数据 ============
天气数据 = {
    '城市': '上海',
    '天气': '--',
    '温度': '--',
    '湿度': '--',
    '风向': '--',
    '风力': '--',
    '最高温': '--',
    '最低温': '--',
    '更新时间': '--',
    '获取状态': '初始化中...'
}

# ============ 获取心知天气数据 ============
def get_seni_weather(_url, _location):
    _url = _url + "&location=" + _location.replace(" ", "%20")
    response = urequests.get(_url)
    json_data = response.json()
    response.close()
    return json_data

# ============ 拉取并解析上海实时天气 ============
def fetch_shanghai_weather():
    global 天气数据
    try:
        w1 = get_seni_weather(NOW_URL, CITY)        # 实时天气
        w2 = get_seni_weather(DAILY_URL, CITY)      # 今日预报
        now = w1["results"][0]["now"]
        daily = w2["results"][0]["daily"][0]
        loc = w1["results"][0]["location"]
        天气数据['城市'] = loc["name"]
        天气数据['天气'] = now["text"]
        天气数据['温度'] = now["temperature"]
        天气数据['湿度'] = now.get("humidity", "--") if isinstance(now, dict) else "--"
        天气数据['风向'] = daily["wind_direction"]
        天气数据['风力'] = daily["wind_scale"]
        天气数据['最高温'] = daily["high"]
        天气数据['最低温'] = daily["low"]
        天气数据['更新时间'] = time.strftime('%H:%M', time.localtime()) if hasattr(time, 'strftime') else '--'
        天气数据['获取状态'] = 'OK'
        print('天气更新成功:', 天气数据['天气'], 天气数据['温度'] + '℃')
        return True
    except Exception as e:
        天气数据['获取状态'] = '获取失败'
        print('天气获取失败:', e)
        return False

# ============ OLED显示刷新 ============
def show_weather():
    oled.fill(0)
    # 第1行：标题 + 城市
    oled.DispChar('上海实时天气', 16, 0, 1)
    # 第2行：天气状况 + 当前温度
    line2 = '天气:' + str(天气数据['天气']) + ' ' + str(天气数据['温度']) + 'C'
    oled.DispChar(line2, 0, 16, 1)
    # 第3行：温度范围 + 风向
    line3 = str(天气数据['最低温']) + '-' + str(天气数据['最高温']) + 'C ' + str(天气数据['风向']) + '风'
    oled.DispChar(line3, 0, 32, 1)
    # 第4行：风力 + 状态/更新时间
    line4 = '风力:' + str(天气数据['风力']) + '级 ' + str(天气数据['更新时间'])
    oled.DispChar(line4, 0, 48, 1)
    oled.show()

# ============ 显示提示信息 ============
def show_message(msg, y=32):
    oled.fill(0)
    oled.DispChar('上海实时天气', 16, 0, 1)
    oled.DispChar(msg, 0, y, 1)
    oled.show()

# ============ 启动：连接WiFi ============
oled.fill(0)
oled.DispChar('上海实时天气', 16, 0, 1)
oled.DispChar('正在连接WiFi...', 8, 32, 1)
oled.show()

my_wifi = wifi()
my_wifi.connectWiFi(WIFI_SSID, WIFI_PASSWORD)

while not my_wifi.sta.isconnected():
    time.sleep_ms(500)

ip = my_wifi.sta.ifconfig()[0]
print('WiFi已连接, IP:', ip)
oled.fill(0)
oled.DispChar('上海实时天气', 16, 0, 1)
oled.DispChar('WiFi已连接', 16, 24, 1)
oled.DispChar('IP:' + ip, 0, 48, 1)
oled.show()
time.sleep(1)

# ============ 首次获取天气 ============
show_message('正在获取天气...', 32)
fetch_shanghai_weather()
show_weather()

# ============ 定时刷新天气(每10分钟) ============
REFRESH_INTERVAL = 10 * 60 * 1000  # 10分钟
last_fetch_time = time.ticks_ms()

# ============ 主循环：定时刷新 + 显示 ============
while True:
    try:
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_fetch_time) >= REFRESH_INTERVAL:
            show_message('更新中...', 32)
            if fetch_shanghai_weather():
                show_weather()
            else:
                show_weather()  # 失败也刷新显示(保留上次数据)
            last_fetch_time = current_time
        # 每500ms刷新一次OLED(显示时间变化等)
        show_weather()
    except Exception as e:
        print('主循环异常:', e)
        show_message('运行异常,重试', 32)
    time.sleep_ms(500)
