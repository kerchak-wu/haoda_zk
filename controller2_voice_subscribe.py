from mpython import *
from machine import UART, Timer
from asr_TTS import ASR_TTS
import radio
import time

# === 好搭掌控2：radio广播接收 + OLED显示 + 语音识别 + 语音合成播报 ===
# 硬件：P15 接 语音识别模块2.0 (UART, 115200)
#       P16 接 语音合成模块V2.1
# 通信：radio广播(无需WiFi)，频道5，接收 "温度=xx" 和 "湿度=xx"
# 唤醒词：智能管家
# 命令词：当前温度(ID=1)、当前湿度(ID=2)

# === 硬件初始化 ===
# 语音识别模块2.0 - P15 (UART, 波特率115200)
asr = machine.UART(1, baudrate=115200, rx=Pin.P15)

# 语音合成模块V2.1 - P16
syn = ASR_TTS(Pin.P16)

# === radio广播初始化 ===
radio.on()
radio.config(channel=5)

# === 全局变量 ===
温度 = 0
湿度 = 0
命令信息 = '等待唤醒...'

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

# === 解析radio消息 "键=值" ===
def radio_recv(msg):
    global 温度, 湿度
    try:
        if not msg:
            return
        text = msg.decode('utf-8') if isinstance(msg, (bytes, bytearray)) else msg
        if '=' not in text:
            return
        key, val = text.split('=', 1)
        if key == '温度':
            温度 = int(val)
        elif key == '湿度':
            湿度 = int(val)
    except:
        pass

# === radio接收定时器 (Timer 13, 20ms周期) ===
tim13 = Timer(13)
def timer13_tick(_):
    try:
        msg = radio.receive()
        if msg:
            radio_recv(msg)
    except:
        pass

tim13.init(period=20, mode=Timer.PERIODIC, callback=timer13_tick)

# === 更新OLED显示 ===
def update_oled():
    oled.fill(0)
    oled.DispChar('掌控2-语音播报', 16, 0, 1)
    oled.DispChar(str('温度：') + str(温度) + str('℃'), 0, 16, 1)
    oled.DispChar(str('湿度：') + str(湿度) + str('%RH'), 0, 32, 1)
    oled.DispChar(命令信息[:10], 0, 48, 1)
    oled.show()

# === 初始化显示 ===
oled.fill(0)
oled.DispChar('掌控2-语音播报', 16, 0, 1)
oled.DispChar('radio监听中...', 16, 32, 1)
oled.show()
time.sleep(1)

# === 主循环 ===
last_oled_update = time.ticks_ms()

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

    # 每500ms刷新一次OLED
    if time.ticks_diff(time.ticks_ms(), last_oled_update) >= 500:
        update_oled()
        last_oled_update = time.ticks_ms()

    time.sleep_ms(10)
