from mpython import *
from machine import UART, Timer
import time

# === 语音控制板载RGB灯 ===
# 硬件连接：P0 接 语音识别模块2.0 (UART, 波特率115200)
# 唤醒词：智能管家
# 命令词示例（需在ASRPRO软件中配置）：
#   ID=1: 打开灯光
#   ID=2: 关闭灯光
#   ID=3: 红灯
#   ID=4: 绿灯
#   ID=5: 蓝灯
#   ID=6: 黄灯
#   ID=7: 紫灯
#   ID=8: 白灯
#   ID=9: 彩虹模式
#   ID=10: 调亮一点
#   ID=11: 调暗一点

# === 硬件初始化 ===
# 语音识别模块2.0 - P0 (UART, 波特率115200)
asr = machine.UART(1, baudrate=115200, rx=Pin(Pin.P0))

# === 全局变量 ===
灯光状态 = False  # False=关灯, True=开灯
当前颜色 = (0, 0, 0)  # RGB当前颜色
亮度倍数 = 1.0  # 亮度调节倍数 (0.2, 0.4, 0.6, 0.8, 1.0)
彩虹模式 = False  # 是否开启彩虹模式
命令信息 = '等待语音命令...'

# === 亮度等级 ===
亮度等级列表 = [0.2, 0.4, 0.6, 0.8, 1.0]
当前亮度索引 = 4  # 默认最亮

# === 预定义颜色 ===
颜色字典 = {
    '红色': (255, 0, 0),
    '绿色': (0, 255, 0),
    '蓝色': (0, 0, 255),
    '黄色': (255, 255, 0),
    '紫色': (255, 0, 255),
    '青色': (0, 255, 255),
    '白色': (255, 255, 255),
    '橙色': (255, 165, 0),
    '粉色': (255, 192, 203)
}

# === RGB控制函数 ===
def 设置RGB颜色(r, g, b, 应用亮度=True):
    """设置RGB灯颜色"""
    global 当前颜色, 彩虹模式
    彩虹模式 = False
    
    if 应用亮度:
        r = int(r * 亮度倍数)
        g = int(g * 亮度倍数)
        b = int(b * 亮度倍数)
    
    当前颜色 = (r, g, b)
    rgb.fill((r, g, b))
    rgb.write()

def 关闭灯光():
    """关闭RGB灯"""
    global 灯光状态, 彩虹模式
    灯光状态 = False
    彩虹模式 = False
    rgb.fill((0, 0, 0))
    rgb.write()

def 打开灯光():
    """打开RGB灯（恢复上次颜色）"""
    global 灯光状态
    灯光状态 = True
    if 当前颜色 == (0, 0, 0):
        设置RGB颜色(255, 255, 255)  # 默认白色
    else:
        r, g, b = 当前颜色
        设置RGB颜色(r, g, b, 应用亮度=False)

def 调亮():
    """增加亮度"""
    global 亮度倍数, 当前亮度索引
    if 当前亮度索引 < len(亮度等级列表) - 1:
        当前亮度索引 += 1
        亮度倍数 = 亮度等级列表[当前亮度索引]
        if 灯光状态:
            r, g, b = 当前颜色
            设置RGB颜色(r, g, b, 应用亮度=False)
        return True
    return False

def 调暗():
    """降低亮度"""
    global 亮度倍数, 当前亮度索引
    if 当前亮度索引 > 0:
        当前亮度索引 -= 1
        亮度倍数 = 亮度等级列表[当前亮度索引]
        if 灯光状态:
            r, g, b = 当前颜色
            设置RGB颜色(r, g, b, 应用亮度=False)
        return True
    return False

# === 彩虹模式 ===
def 彩虹模式循环():
    """彩虹渐变效果"""
    global 彩虹模式, 灯光状态
    
    if not 彩虹模式 or not 灯光状态:
        return
    
    # 彩虹色循环：红->橙->黄->绿->青->蓝->紫->红
    彩虹色列表 = [
        (255, 0, 0),    # 红
        (255, 127, 0),  # 橙
        (255, 255, 0),  # 黄
        (0, 255, 0),    # 绿
        (0, 255, 255),  # 青
        (0, 0, 255),    # 蓝
        (255, 0, 255)   # 紫
    ]
    
    for 颜色 in 彩虹色列表:
        if not 彩虹模式 or not 灯光状态:
            break
        r, g, b = 颜色
        设置RGB颜色(r, g, b)
        time.sleep_ms(500)

# === 读取ASR命令ID ===
def asr_read():
    """读取语音识别模块返回的命令ID"""
    asr_data = asr.read()
    if asr_data is not None:
        return asr_data[-1]  # 取最后一字节作为命令ID
    return -1

# === 处理语音命令 ===
def 处理语音命令(cmd_id):
    """根据命令ID执行相应操作"""
    global 命令信息, 灯光状态, 彩虹模式
    
    # ID=1: 打开灯光
    if cmd_id == 1:
        命令信息 = '命令：打开灯光'
        打开灯光()
    
    # ID=2: 关闭灯光
    elif cmd_id == 2:
        命令信息 = '命令：关闭灯光'
        关闭灯光()
    
    # ID=3: 红灯
    elif cmd_id == 3:
        命令信息 = '命令：红灯'
        灯光状态 = True
        设置RGB颜色(255, 0, 0)
    
    # ID=4: 绿灯
    elif cmd_id == 4:
        命令信息 = '命令：绿灯'
        灯光状态 = True
        设置RGB颜色(0, 255, 0)
    
    # ID=5: 蓝灯
    elif cmd_id == 5:
        命令信息 = '命令：蓝灯'
        灯光状态 = True
        设置RGB颜色(0, 0, 255)
    
    # ID=6: 黄灯
    elif cmd_id == 6:
        命令信息 = '命令：黄灯'
        灯光状态 = True
        设置RGB颜色(255, 255, 0)
    
    # ID=7: 紫灯
    elif cmd_id == 7:
        命令信息 = '命令：紫灯'
        灯光状态 = True
        设置RGB颜色(255, 0, 255)
    
    # ID=8: 白灯
    elif cmd_id == 8:
        命令信息 = '命令：白灯'
        灯光状态 = True
        设置RGB颜色(255, 255, 255)
    
    # ID=9: 彩虹模式
    elif cmd_id == 9:
        命令信息 = '命令：彩虹模式'
        彩虹模式 = True
        灯光状态 = True
    
    # ID=10: 调亮一点
    elif cmd_id == 10:
        命令信息 = '命令：调亮'
        if 调亮():
            命令信息 = '命令：调亮成功'
        else:
            命令信息 = '命令：已最亮'
    
    # ID=11: 调暗一点
    elif cmd_id == 11:
        命令信息 = '命令：调暗'
        if 调暗():
            命令信息 = '命令：调暗成功'
        else:
            命令信息 = '命令：已最暗'

# === 更新OLED显示 ===
def update_oled():
    """更新OLED屏幕显示"""
    oled.fill(0)
    oled.DispChar('语音控制RGB灯', 16, 0, 1)
    
    # 显示当前状态
    状态文本 = '状态：开灯' if 灯光状态 else '状态：关灯'
    oled.DispChar(状态文本, 0, 16, 1)
    
    # 显示亮度
    亮度百分比 = int(亮度倍数 * 100)
    oled.DispChar(str('亮度：') + str(亮度百分比) + str('%'), 0, 32, 1)
    
    # 显示当前命令
    oled.DispChar(命令信息[:12], 0, 48, 1)
    oled.show()

# === 初始化显示 ===
oled.fill(0)
oled.DispChar('语音控制RGB灯', 16, 0, 1)
oled.DispChar('P0接语音模块', 16, 16, 1)
oled.DispChar('唤醒词：智能管家', 0, 32, 1)
oled.DispChar('系统就绪', 32, 48, 1)
oled.show()

# 初始关闭灯光
关闭灯光()
time.sleep(1)

# === 主循环 ===
last_oled_update = time.ticks_ms()
last_rainbow_update = time.ticks_ms()

print('语音控制RGB灯系统已启动')
print('P0 -> 语音识别模块2.0 (UART 115200)')
print('唤醒词：智能管家')

while True:
    # 检查ASR是否有新命令
    if asr.any():
        cmd_id = asr_read()
        if cmd_id >= 1:
            time.sleep_ms(200)  # 防抖延迟
            处理语音命令(cmd_id)
            update_oled()
    
    # 彩虹模式循环（每2秒切换一次颜色）
    if 彩虹模式 and 灯光状态:
        if time.ticks_diff(time.ticks_ms(), last_rainbow_update) >= 2000:
            彩虹模式循环()
            last_rainbow_update = time.ticks_ms()
    
    # 每500ms刷新一次OLED
    if time.ticks_diff(time.ticks_ms(), last_oled_update) >= 500:
        update_oled()
        last_oled_update = time.ticks_ms()
    
    # 短暂休眠，让出CPU
    time.sleep_ms(10)