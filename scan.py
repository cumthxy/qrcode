import requests
import json
import asyncio, evdev
from evdev import InputDevice, categorize, ecodes

def post_data(message):
    url=""
    requests.post(url,data=json.dumps({"message":message}))
    
    
# 解码 
scancodes = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u':',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

capscodes = {
    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT',  57: u' ', 100: u'RALT'
}


async def print_events(device):
    caps = False
    bufs = ""
    async for event in device.async_read_loop():
        if event.type == ecodes.EV_KEY:
            data = categorize(event)
            if data.scancode == 42 or data.scancode==54:
                if data.keystate == 1:
                    caps = True
                if data.keystate == 0:
                    caps = False
            if data.keystate == 1:
                # 判断SHIFT键是不是按住的，如果是按住的就读取大写字母
                if caps:
                    key_lookup =capscodes.get(data.scancode)
                else:
                    key_lookup = scancodes.get(data.scancode)
                # SHFT，CTRL，TAB属于特殊按键，不计算在扫码内容结果中
                if (data.scancode != 42) and (data.scancode != 28) and (data.scancode != 15)and (data.scancode != 54):
                    bufs += key_lookup  
                # 回车结束
                if(data.scancode==evdev.ecodes.KEY_ENTER):  # Print it all out!
                    print(bufs)
                    
# 列出 usb 设备
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

for device in devices:
    print(device.path, device.name, device.phys)

for device in devices:
	asyncio.ensure_future(print_events(device))
 
loop = asyncio.get_event_loop()
loop.run_forever()
                  
                    


