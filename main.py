# Import many things
from machine import Pin, SoftI2C
import ssd1306
import network
import ntptime
import time
import urequests
import json

# oled size (usually just keep this)
oled_width = 128
oled_height = 64

# i2c pin(change if you want)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# wifi (MUST SET!!! USE FOR NTP)
wifi_ssid = ''
wifi_password = ''

# NTP Server 
ntp_server = 'stdtime.gov.hk'
ntptime.NTP_DELTA = 28800

nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect(wifi_ssid, wifi_password)

ntptime.host = ntp_server


def sync_time():
    # For UTC+8
    ntptime.NTP_DELTA = 3155644800
    ntptime.host = ntp_server
    while True:
        try:
            ntptime.settime()
            break
        except OSError:
            oled.fill(0)
            oled.text("Failed to sync time. Retrying...", 0, 10)
            time.sleep(1)


temp = "Err"


def weather():
    global temp
    global utime
    try:
        r = urequests.get("http://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc")
        weather_data = json.loads(r.text)
        temperature_data = weather_data["temperature"]["data"]
        for entry in temperature_data:
            """
            For example I live in 沙田, you can choose:
            京士柏,香港天文台,黃竹坑,打鼓嶺,流浮山,大埔,沙田,屯門,將軍澳,西貢,長洲,赤鱲角,青衣,石崗,荃灣可觀,
            荃灣城門谷,香港公園,筲箕灣,九龍城,跑馬地,黃大仙,赤柱,觀塘,深水埗,啟德,跑道,公園,元朗,公園,大美督
            """
            if entry["place"] == "沙田":
                temperature = entry["value"]
                unit = entry["unit"]
                utime = weather_data["temperature"]["recordTime"]
                temp = str(temperature) + str(unit)
                print(temp + utime)
                if temperature > 25 and temperature <= 30:
                    emoji = ":/"
                elif temperature >= 18 and temperature <= 25:
                    emoji = ":)"
                elif temperature < 18 or temperature > 30:
                    emoji = ":("
                break
    except Exception as e:
        print("Error accessing weather API:", str(e))
        temp = "Err"


weather()

sync_time()

counter = 0
counter_weather = 0

while True:

    oled.fill(0)

    current_time = time.localtime()
    current_time = list(current_time)
    current_time[3] = (current_time[3] + 8) % 24
    current_time = tuple(current_time)

    formatted_time = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])
    formatted_date = "{:04d}-{:02d}-{:02d}".format(current_time[0], current_time[1], current_time[2])

    oled.text("Time: " + formatted_time, 0, 5)
    oled.text("Date: " + formatted_date, 0, 20)
    oled.text("Weather: " + str(temp), 0, 35)
    oled.text(str(utime), 0, 50)

    oled.show()

    time.sleep(1)

    counter += 1
    counter_weather += 1
    if counter >= 20000:
        sync_time()
        weather()
        counter = 0
    if counter_weather >= 9999:
        weather()
        counter_weather = 0
