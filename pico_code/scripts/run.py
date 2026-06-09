import asyncio
from pico_logger import PicoLogger

def main():
    from setup_connection import start_server_tcp, start_server_udp

    print('Starting display program')

    print('Establishing WiFi connection')
    ip = start_wifi_connection()

    if ip is None:
        return
    
    tcp_sock = start_server_tcp(ip, 8080)
    udp_sock = start_server_udp(ip, 5005)

    logger = PicoLogger(udp_sock)

    

def start_wifi_connection():

    from wifi_config_handler import get_wifi_config
    from wifi_connection_handler import connect_to_wifi, disconnect_from_wifi

    ssid, psswrd = get_wifi_config()

    try:
        ip = connect_to_wifi(ssid, psswrd)
    except:
        disconnect_from_wifi()
        print('Could not connect to network')
        return None
    
    return ip

async def run_display_loop(sock, logger):

    while True:

        try:
            conn, addr = sock.accept()
            conn.setblocking(False)
            conn.send

        except OSError:
            await asyncio.sleep(0.1)