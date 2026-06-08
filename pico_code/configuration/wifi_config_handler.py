import ujson

WIFI_CONFIG_FILE_NAME = 'wifi_config.json'

def SaveWiFiConfig(ssid, psswrd):

    config = {
        'ssid': ssid,
        'psswrd': psswrd
    }

    with open(WIFI_CONFIG_FILE_NAME, 'w') as f:
        ujson.dump(config, f)

def GetWiFiConfig():
    with open(WIFI_CONFIG_FILE_NAME, 'r') as f:
        config = ujson.load(f)
    return config['ssid'], config['password']