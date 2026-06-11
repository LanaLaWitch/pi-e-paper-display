import asyncio
from pico_logger import PicoLogger
from refresh_monitor import RefreshMonitor
from display_packet_decoder import get_display_frame_buffer
from epaper_213_v4 import LANDSCAPE, EPD_2in13_V4_Landscape, EPD_2in13_V4_Portrait
from run_display import process_display_buffer

DISPLAY_TIMEOUT_H = 18
MIN_REFRESH_RATE_M = 3


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
    refresh_monitor = RefreshMonitor(DISPLAY_TIMEOUT_H, MIN_REFRESH_RATE_M)

    asyncio.run(run_all_tasks(tcp_sock, logger, refresh_monitor))


async def run_all_tasks(sock, logger, refresh_monitor):
    await asyncio.gather(
        run_display_loop(sock, logger, refresh_monitor)
    )

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

async def run_display_loop(sock, logger, refresh_monitor):

    while True:

        try:
            frame_buffer = await listen_for_data(sock)

            if frame_buffer.orientation == LANDSCAPE:
                epd = EPD_2in13_V4_Landscape()
            else:
                epd = EPD_2in13_V4_Portrait()
            
            refresh_monitor.reset_monitor()
            await process_display_buffer(epd, frame_buffer)
            
        except OSError:
            await asyncio.sleep(0.1)

async def listen_for_data(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    conn.send(b'READY')

    received_data_buffer = await get_display_frame_buffer(conn)
    return received_data_buffer
