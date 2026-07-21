from mpython import *
from machine import Timer
import dht
import time

dht11 = dht.DHT11(Pin(Pin.P0))

tim13 = Timer(13)
def timer13_tick(_):
    try:
        dht11.measure()
    except:
        pass

tim13.init(period=1000, mode=Timer.PERIODIC, callback=timer13_tick)

oled.fill(0)
oled.DispChar('DHT11温湿度监测', 16, 0, 1)
oled.DispChar('正在初始化...', 16, 32, 1)
oled.show()
time.sleep(1)

while True:
    try:
        温度 = dht11.temperature()
        湿度 = dht11.humidity()
        oled.fill(0)
        oled.DispChar('DHT11温湿度监测', 16, 0, 1)
        oled.DispChar(str('温度：') + str(温度) + str('℃'), 0, 24, 1)
        oled.DispChar(str('湿度：') + str(湿度) + str('%RH'), 0, 40, 1)
        oled.show()
    except:
        oled.fill(0)
        oled.DispChar('DHT11温湿度监测', 16, 0, 1)
        oled.DispChar('读取失败,请检查', 8, 32, 1)
        oled.show()
    time.sleep(1)
