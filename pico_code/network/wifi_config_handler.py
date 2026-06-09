import ujson

WIFI_CONFIG_FILE_NAME = 'wifi_config.json'


def save_wifi_config(ssid, psswrd):
    config = {
        'ssid': ssid,
        'psswrd': psswrd
    }

    with open(WIFI_CONFIG_FILE_NAME, 'w') as f:
        ujson.dump(config, f)


def get_wifi_config():
    with open(WIFI_CONFIG_FILE_NAME, 'r') as f:
        config = ujson.load(f)
    return config['ssid'], config['password']
