# haoda_zk
好搭掌控项目 with Trae work

## 项目资料

- <a href="C__好搭Block_resources_wulink_python.pdf" download>📄 好搭掌控编程手册.pdf</a> — 好搭掌控编程手册
- <a href="extracted_code.txt" download>📄 范例代码1.txt</a> — 好搭掌控范例代码（1）
- <a href="extracted_code3.txt" download>📄 范例代码2.txt</a> — 好搭掌控范例代码（2）
- <a href="extracted_code5.txt" download>📄 范例代码3.txt</a> — 好搭掌控范例代码（3）

## 项目列表

| 序号 | 项目 | 文件 | 文档 |
| --- | --- | --- | --- |
| 1 | 好搭智眼Pro颜色识别OLED显示与RGB联动 | [haoda_aieye_color_oled.py](haoda_aieye_color_oled.py) | <a href="好搭智眼Pro颜色识别说明文档.md" download>📄 项目文档</a> |
| 2 | 触摸键控制板载RGB灯 | [touch_rgb_control.py](touch_rgb_control.py) | <a href="touch_rgb_control_说明文档.md" download>📄 项目文档</a> |
| 3 | DHT11温湿度OLED显示 | [dht11_oled_display.py](dht11_oled_display.py) | — |
| 4 | 上海天气OLED显示 | [shanghai_weather_oled.py](shanghai_weather_oled.py) | <a href="上海天气OLED显示系统说明.md" download>📄 项目文档</a> |
| 5 | 温湿度语音播报（单板MQTT版） | [voice_temp_humidity.py](voice_temp_humidity.py) | — |
| 6 | 双板无线温湿度语音播报（radio版） | [controller1_dht11_publish.py](controller1_dht11_publish.py) / [controller2_voice_subscribe.py](controller2_voice_subscribe.py) | <a href="温湿度语音播报系统说明.md" download>📄 项目文档</a> |
| 7 | RGB呼吸灯 | [rgb_breath_led.py](rgb_breath_led.py) | — |
| 8 | RGB按键控制 | [rgb_button_control.py](rgb_button_control.py) | — |
| 9 | WiFi控制RGB灯 | [wifi_rgb_control.py](wifi_rgb_control.py) | — |
| 10 | BLE控制RGB灯 | [ble_rgb_control.py](ble_rgb_control.py) | — |
| 11 | AP模式RGB控制 | [ap_rgb_control.py](ap_rgb_control.py) | — |

<style>
  /* ===== 页面主体宽度设为 70%，居中 ===== */
  .main-content {
    max-width: 70% !important;
    margin: 0 auto !important;
    padding: 0 20px !important;
  }

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

  /* ===== 表头样式（字体更大） ===== */
  .main-content table thead th {
    background: linear-gradient(135deg, #159957, #155799) !important;
    color: #fff !important;
    font-weight: 700 !important;
    font-size: 22px !important;
    padding: 16px 20px !important;
    text-align: center !important;
    letter-spacing: 0.5px !important;
  }

  /* ===== 单元格通用样式 ===== */
  .main-content table td,
  .main-content table th {
    padding: 14px 18px !important;
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

  /* ===== 列宽分配（新增序号列，文档列适当减小） ===== */
  .main-content table th:nth-child(1),
  .main-content table td:nth-child(1) {
    width: 8% !important;      /* 序号列 */
  }
  .main-content table th:nth-child(2),
  .main-content table td:nth-child(2) {
    width: 35% !important;     /* 项目列 */
  }
  .main-content table th:nth-child(3),
  .main-content table td:nth-child(3) {
    width: 32% !important;     /* 文件列 */
  }
  .main-content table th:nth-child(4),
  .main-content table td:nth-child(4) {
    width: 25% !important;     /* 文档列（减小） */
  }

  /* ===== 文档列（第四列）居中 ===== */
  .main-content table th:nth-child(4),
  .main-content table td:nth-child(4) {
    text-align: center !important;
  }

  /* ===== 文件链接样式（.py 文件） ===== */
  .main-content table td a[href$=".py"] {
    font-family: 'Consolas', 'Monaco', monospace !important;
    font-size: 15px !important;
    background: #f0f2f5 !important;
    padding: 4px 12px !important;
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
    padding: 6px 20px !important;
    background: linear-gradient(135deg, #159957, #155799) !important;
    color: #fff !important;
    border-radius: 24px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    text-decoration: none !important;
    transition: transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 2px 6px rgba(21, 87, 153, 0.2) !important;
  }

  .main-content table td a[href$=".md"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px rgba(21, 87, 153, 0.4) !important;
    text-decoration: none !important;
  }

  /* ===== “—” 占位符样式（居中后也适用） ===== */
  .main-content table td:contains("—") {
    color: #b0b8c4 !important;
    font-size: 16px !important;
  }
</style>
