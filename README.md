# haoda_zk
好搭掌控项目 with Trae work

## 项目列表

| 项目 | 文件 | 说明文档 |
| --- | --- | --- |
| 好搭智眼Pro颜色识别OLED显示与RGB联动 | [haoda_aieye_color_oled.py](haoda_aieye_color_oled.py) | <a href="好搭智眼Pro颜色识别说明文档.md" download>📄 说明文档</a> |
| 触摸键控制板载RGB灯 | [touch_rgb_control.py](touch_rgb_control.py) | <a href="touch_rgb_control_说明文档.md" download>📄 说明文档</a> |
| DHT11温湿度OLED显示 | [dht11_oled_display.py](dht11_oled_display.py) | — |
| 上海天气OLED显示 | [shanghai_weather_oled.py](shanghai_weather_oled.py) | <a href="上海天气OLED显示系统说明.md" download>📄 说明文档</a> |
| 温湿度语音播报（单板MQTT版） | [voice_temp_humidity.py](voice_temp_humidity.py) | — |
| 双板无线温湿度语音播报（radio版） | [controller1_dht11_publish.py](controller1_dht11_publish.py) / [controller2_voice_subscribe.py](controller2_voice_subscribe.py) | <a href="温湿度语音播报系统说明.md" download>📄 说明文档</a> |
| RGB呼吸灯 | [rgb_breath_led.py](rgb_breath_led.py) | — |
| RGB按键控制 | [rgb_button_control.py](rgb_button_control.py) | — |
| WiFi控制RGB灯 | [wifi_rgb_control.py](wifi_rgb_control.py) | — |
| BLE控制RGB灯 | [ble_rgb_control.py](ble_rgb_control.py) | — |
| AP模式RGB控制 | [ap_rgb_control.py](ap_rgb_control.py) | — |

<style>
  /* ===== 表格整体样式 ===== */
  .main-content table {
    width: 100% !important;
    border-collapse: separate !important;
    border-spacing: 0 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08) !important;
    display: table !important;
    overflow-x: visible !important;
  }

  /* ===== 表头样式 ===== */
  .main-content table thead th {
    background: linear-gradient(135deg, #159957, #155799) !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 14px 16px !important;
    text-align: center !important;
    letter-spacing: 0.5px !important;
  }

  /* ===== 单元格通用样式 ===== */
  .main-content table td,
  .main-content table th {
    padding: 12px 16px !important;
    white-space: normal !important;
    word-break: break-word !important;
    vertical-align: middle !important;
  }

  /* ===== 表格行交替色 ===== */
  .main-content table tbody tr:nth-child(even) {
    background-color: #f8f9fb !important;
  }

  .main-content table tbody tr:nth-child(odd) {
    background-color: #ffffff !important;
  }

  /* ===== 行悬停高亮 ===== */
  .main-content table tbody tr:hover {
    background-color: #eaf4f0 !important;
    transition: background-color 0.2s ease !important;
  }

  /* ===== 列宽分配 ===== */
  .main-content table th:nth-child(1),
  .main-content table td:nth-child(1) {
    width: 35% !important;
  }
  .main-content table th:nth-child(2),
  .main-content table td:nth-child(2) {
    width: 35% !important;
  }
  .main-content table th:nth-child(3),
  .main-content table td:nth-child(3) {
    width: 30% !important;
  }

  /* ===== 文件链接样式（.py 文件） ===== */
  .main-content table td a[href$=".py"] {
    font-family: 'Consolas', 'Monaco', monospace !important;
    font-size: 13px !important;
    background: #f0f2f5 !important;
    padding: 2px 10px !important;
    border-radius: 6px !important;
    border: 1px solid #e1e4e8 !important;
    color: #0366d6 !important;
    text-decoration: none !important;
    display: inline-block !important;
    transition: background 0.2s !important;
  }

  .main-content table td a[href$=".py"]:hover {
    background: #e1e4e8 !important;
    text-decoration: none !important;
  }

  /* ===== 说明文档下载链接样式（.md 文件） ===== */
  .main-content table td a[href$=".md"] {
    display: inline-block !important;
    padding: 4px 16px !important;
    background: linear-gradient(135deg, #159957, #155799) !important;
    color: #fff !important;
    border-radius: 20px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-decoration: none !important;
    transition: transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 2px 6px rgba(21, 87, 153, 0.2) !important;
  }

  .main-content table td a[href$=".md"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(21, 87, 153, 0.35) !important;
    text-decoration: none !important;
  }

  /* ===== “—” 占位符样式 ===== */
  .main-content table td:contains("—") {
    color: #b0b8c4 !important;
    font-size: 14px !important;
  }
</style>
