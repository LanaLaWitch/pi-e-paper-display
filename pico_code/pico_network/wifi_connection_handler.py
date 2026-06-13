import network
import time

HOSTNAME = 'pico-epaper-display'

def scan_for_networks():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print('Scanning for networks...')
    found_networks = wlan.scan()
    print(f'{len(found_networks)} were found')

    for i, net in enumerate(found_networks):
        print(f'{i}: {net}')

    wlan.active(False)
    return found_networks


def connect_to_wifi(ssid, psswrd):

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print(f'Connecting to network: {ssid}...')
    wlan.connect(ssid, psswrd)

    timeout = 0
    while timeout < 10 and not wlan.isconnected() and wlan.status() >= 0:
        timeout += 1
        time.sleep(1)

    if not wlan.isconnected() or wlan.status() != 3:
        print(f'Connection failed after {timeout} seconds. Status {wlan.status()}')
        wlan.active(False)
        return None

    status = wlan.ifconfig()
    print(f'Connection successful. IP: {status[0]}')

    return status[0]


def disconnect_from_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print('Disconnecting from network')
    wlan.disconnect()

    wlan.active(False)


def test_connect_to_wifi(ssid, psswrd):
    connection_success = connect_to_wifi(ssid, psswrd)

    if connection_success is not None:
        disconnect_from_wifi()

    return connection_success is not None
