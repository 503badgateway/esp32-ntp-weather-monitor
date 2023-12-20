
<img src="https://github.com/503badgateway/esp32-ntp-weather-monitor/blob/main/img.jpeg?raw=true" style="width: 25%"></img>
# esp32-ntp-weather-monitor  
 - Shows Weather (Every 9999s)
 - Shows Time
 - NTP Synchronize time (Every 20000s)
 - Show emojis based on the weather :) / or :/ or :(

Todo List:
 - More features
# Build one
*Before you start, you need to know that this project only uses HKO API. If you want to use it in another country, you may need to modify the code.*

Things You need:    
 - ESP32(May also work on esp8266)(For me: esp32 devkit v1) 
 - More than 4 wire  
 - ssd1306 monitor  

Connent ssd1306 like this:
<img src="https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/05/ESP32_OLED.png?w=873&quality=100&strip=all&ssl=1" style="width: 25%"></img>  

Open **Thonny** and flash *main.py* and [ssd1306.py](https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py)  
**Remember set your wifi first**


