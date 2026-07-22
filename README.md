# haoda_zk
好搭掌控项目 with Trae work

## 项目列表

<style>
  /* 强制表格占满宽度，消除横向滚动条 */
  .markdown-body table,
  table {
    display: table !important;
    width: 100% !important;
    overflow-x: visible !important;
  }
  
  .markdown-body table td,
  .markdown-body table th,
  table td,
  table th {
    white-space: normal !important;
    word-break: break-word !important;
  }
  
  /* 针对 cayman 主题的表格容器 */
  .main-content table {
    display: table !important;
    width: 100% !important;
    overflow-x: visible !important;
  }
  
  .main-content table td,
  .main-content table th {
    white-space: normal !important;
    word-break: break-word !important;
  }
</style>

| 项目 | 文件 | 说明文档 |
| --- | --- | --- |
| 好搭智眼Pro颜色识别OLED显示与RGB联动 | [haoda_aieye_color_oled.py](haoda_aieye_color_oled.py) | [好搭智眼Pro颜色识别说明文档.md](好搭智眼Pro颜色识别说明文档.md) |
| 触摸键控制板载RGB灯 | [touch_rgb_control.py](touch_rgb_control.py) | [touch_rgb_control_说明文档.md](touch_rgb_control_说明文档.md) |
| DHT11温湿度OLED显示 | [dht11_oled_display.py](dht11_oled_display.py) | — |
| 上海天气OLED显示 | [shanghai_weather_oled.py](shanghai_weather_oled.py) | [上海天气OLED显示系统说明.md](上海天气OLED显示系统说明.md) |
| 温湿度语音播报（单板MQTT版） | [voice_temp_humidity.py](voice_temp_humidity.py) | — |
| 双板无线温湿度语音播报（radio版） | [controller1_dht11_publish.py](controller1_dht11_publish.py) / [controller2_voice_subscribe.py](controller2_voice_subscribe.py) | [温湿度语音播报系统说明.md](温湿度语音播报系统说明.md) |
| RGB呼吸灯 | [rgb_breath_led.py](rgb_breath_led.py) | — |
| RGB按键控制 | [rgb_button_control.py](rgb_button_control.py) | — |
| WiFi控制RGB灯 | [wifi_rgb_control.py](wifi_rgb_control.py) | — |
| BLE控制RGB灯 | [ble_rgb_control.py](ble_rgb_control.py) | — |
| AP模式RGB控制 | [ap_rgb_control.py](ap_rgb_control.py) | — |
