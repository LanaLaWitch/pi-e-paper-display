import network
import time

def ScanForNetworks():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print('Scanning for networks...')
    found_networks = wlan.scan()
    print(f'{len(found_networks)} were found')

    for i in range(len(found_networks)):
        print(f'{i}: {found_networks[i]}')

    wlan.active(False)
    return found_networks

def ConnectToWiFi(ssid, psswrd):

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
        return False
    
    status = wlan.ifconfig()
    print(f'Connection successful. IP: {status[0]}')

    wlan.active(False)
    return True

def DisconnectFromWiFi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print('Disconnecting from network')
    wlan.disconnect()

    wlan.active(False)

def TestConnectToWiFi(ssid, psswrd):

    connection_success = ConnectToWiFi(ssid, psswrd)

    if connection_success:
        DisconnectFromWiFi()

    return connection_success