from mpython import *
from machine import UART, Timer
from asr_TTS import ASR_TTS
from umqtt.simple import MQTTClient
import dht
import time

# === 硬件初始化 ===
# DHT11温湿度传感器 - P0
dht11 = dht.DHT11(Pin(Pin.P0))

# 语音识别模块2.0 - P15 (UART, 波特率115200)
# 唤醒词：智能管家
# 命令词：当前温度(ID=1)、当前湿度(ID=2)
# 注：ID需与ASR模块实际配置一致，可在ASRPRO软件中查看
asr = machine.UART(1, baudrate=115200, rx=Pin.P15)

# 语音合成模块V2.1 - P16
syn = ASR_TTS(Pin.P16)

# === WiFi 与 MQTT 配置 ===
# WiFi：haoda7 / 密码：0123456789
# MQTT服务器：192.168.2.251:1883
# 发布主题：topic/temperature（温度）、topic/humidity（湿度）
my_wifi = wifi()
my_wifi.connectWiFi('haoda7', '0123456789')
mqtt = MQTTClient('', '192.168.2.251', 1883, '', '', 30)
MQTT_TOPIC_TEMP = 'topic/temperature'
MQTT_TOPIC_HUM = 'topic/humidity'

# === 全局变量 ===
温度 = 0
湿度 = 0
命令信息 = '等待唤醒...'
mqtt_connected = False

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

# === 语音合成模块设置 ===
syn.volume(9)  # 音量范围 0-9

# === 读取ASR命令ID ===
def asr_read():
    asr_data = asr.read()
    if asr_data is not None:
        return asr_data[-1]  # 取最后一字节作为命令ID
    return -1

# === 数字转中文读法 (0-100) ===
# 解决TTS将"50"读成"五零"而非"五十"的问题
def 数字转中文(num):
    数字 = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    num = int(num)
    if num == 0:
        return '零'
    if num < 10:
        return 数字[num]
    if num == 10:
        return '十'
    if num < 20:
        return '十' + 数字[num % 10]
    if num < 100:
        十位 = num // 10
        个位 = num % 10
        if 个位 == 0:
            return 数字[十位] + '十'
        return 数字[十位] + '十' + 数字[个位]
    if num == 100:
        return '一百'
    return str(num)

# === 更新OLED显示 ===
def update_oled():
    oled.fill(0)
    oled.DispChar('语音播报温湿度', 16, 0, 1)
    oled.DispChar(str('温度：') + str(温度) + str('℃'), 0, 16, 1)
    oled.DispChar(str('湿度：') + str(湿度) + str('%RH'), 0, 32, 1)
    # 第4行：MQTT状态(连接/断开) + 最近命令
    mqtt_status = 'MQTT:OK ' if mqtt_connected else 'MQTT:OFF'
    oled.DispChar(mqtt_status + 命令信息[:8], 0, 48, 1)
    oled.show()

# === 初始化显示 ===
oled.fill(0)
oled.DispChar('语音播报温湿度', 16, 0, 1)
oled.DispChar('连接WiFi中...', 16, 32, 1)
oled.show()

# === 等待WiFi连接 ===
while not my_wifi.sta.isconnected():
    time.sleep_ms(100)
oled.fill(0)
oled.DispChar('IP:' + str(my_wifi.sta.ifconfig()[0]), 0, 0, 1)
oled.DispChar('连接MQTT中...', 16, 32, 1)
oled.show()

# === 连接MQTT服务器 ===
try:
    mqtt.connect()
    mqtt_connected = True
    print('MQTT Connected to 192.168.2.251')
except Exception as e:
    mqtt_connected = False
    print('MQTT Connect Failed:', e)

time.sleep(1)

# === MQTT发布温湿度 ===
def mqtt_publish_temp_humidity():
    global mqtt_connected
    if not mqtt_connected:
        return False
    try:
        mqtt.publish(MQTT_TOPIC_TEMP, str(温度))
        mqtt.publish(MQTT_TOPIC_HUM, str(湿度))
        return True
    except Exception as e:
        print('MQTT Publish Failed:', e)
        mqtt_connected = False
        return False

# === 重连MQTT ===
def mqtt_reconnect():
    global mqtt_connected
    try:
        mqtt.connect()
        mqtt_connected = True
        print('MQTT Reconnected')
    except:
        mqtt_connected = False

# === 主循环 ===
last_oled_update = time.ticks_ms()
last_mqtt_publish = time.ticks_ms()
last_mqtt_reconnect = time.ticks_ms()
MQTT_PUBLISH_INTERVAL = 5000   # 温湿度发布间隔：5秒
MQTT_RECONNECT_INTERVAL = 10000  # 重连尝试间隔：10秒

while True:
    # 检查ASR是否有新命令
    if asr.any():
        cmd_id = asr_read()
        # 命令词"当前温度" - ID 1
        if cmd_id == 1:
            time.sleep_ms(500)  # 防抖延迟
            命令信息 = '命令：当前温度'
            update_oled()
            syn.set_code(0x04)
            syn.play(bytes(str('当前温度为') + 数字转中文(温度) + str('摄氏度'), 'utf-8'))
            syn.set_code(0x00)
        # 命令词"当前湿度" - ID 2
        elif cmd_id == 2:
            time.sleep_ms(500)  # 防抖延迟
            命令信息 = '命令：当前湿度'
            update_oled()
            syn.set_code(0x04)
            syn.play(bytes(str('当前湿度为百分之') + 数字转中文(湿度), 'utf-8'))
            syn.set_code(0x00)

    # 每5秒发布一次温湿度到MQTT
    if time.ticks_diff(time.ticks_ms(), last_mqtt_publish) >= MQTT_PUBLISH_INTERVAL:
        if not mqtt_publish_temp_humidity():
            # 发布失败，记录状态
            命令信息 = 'MQTT发布失败'
        last_mqtt_publish = time.ticks_ms()

    # MQTT断线时定期重连
    if not mqtt_connected and time.ticks_diff(time.ticks_ms(), last_mqtt_reconnect) >= MQTT_RECONNECT_INTERVAL:
        mqtt_reconnect()
        last_mqtt_reconnect = time.ticks_ms()

    # 每500ms刷新一次OLED
    if time.ticks_diff(time.ticks_ms(), last_oled_update) >= 500:
        update_oled()
        last_oled_update = time.ticks_ms()

    # 短暂休眠，让出CPU
    time.sleep_ms(10)
