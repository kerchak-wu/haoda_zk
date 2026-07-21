from mpython import *
from machine import Timer
import radio
import dht
import time

# === 好搭掌控1：DHT11采集 + OLED显示 + radio广播发送 ===
# 硬件：P0 接 DHT11温湿度传感器
# 通信：radio广播(无需WiFi)，频道5，发送 "温度=xx" 和 "湿度=xx"

# === 硬件初始化 ===
# DHT11温湿度传感器 - P0
dht11 = dht.DHT11(Pin(Pin.P0))

# === radio广播初始化 ===
radio.on()
radio.config(channel=5)

# === 全局变量 ===
温度 = 0
湿度 = 0

# === DHT11定时采样 (Timer 13, 1秒周期) ===
tim13 = Timer(13)
def timer13_tick(_):
    global 温度, 湿度
    try:
        dht11.measure()
        温度 = dht11.temperature()
        湿度 = dht11.humidity()
    except:
        pass

tim13.init(period=1000, mode=Timer.PERIODIC, callback=timer13_tick)

# === 更新OLED显示 ===
def update_oled():
    oled.fill(0)
    oled.DispChar('掌控1-温湿度采集', 8, 0, 1)
    oled.DispChar(str('温度：') + str(温度) + str('℃'), 0, 16, 1)
    oled.DispChar(str('湿度：') + str(湿度) + str('%RH'), 0, 32, 1)
    oled.DispChar('广播发送中...', 0, 48, 1)
    oled.show()

# === 初始化显示 ===
oled.fill(0)
oled.DispChar('掌控1-温湿度采集', 8, 0, 1)
oled.DispChar('radio广播就绪', 16, 32, 1)
oled.show()
time.sleep(1)

# === 主循环 ===
last_oled_update = time.ticks_ms()
last_broadcast = time.ticks_ms()
BROADCAST_INTERVAL = 2000  # 广播间隔：2秒

while True:
    # 每2秒广播一次温湿度
    if time.ticks_diff(time.ticks_ms(), last_broadcast) >= BROADCAST_INTERVAL:
        try:
            radio.send(str('温度') + '=' + str(温度))
            radio.send(str('湿度') + '=' + str(湿度))
        except Exception as e:
            print('Broadcast Failed:', e)
        last_broadcast = time.ticks_ms()

    # 每500ms刷新一次OLED
    if time.ticks_diff(time.ticks_ms(), last_oled_update) >= 500:
        update_oled()
        last_oled_update = time.ticks_ms()

    time.sleep_ms(10)
