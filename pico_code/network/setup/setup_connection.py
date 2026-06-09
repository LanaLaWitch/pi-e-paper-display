def start_server(port):
    from wifi_config_handler import get_wifi_config
    from wifi_connection_handler import connect_to_wifi, disconnect_from_wifi
    from socket_handler import build_socket_tcp

    ssid, psswrd = get_wifi_config()

    try:
        ip = connect_to_wifi(ssid, psswrd)
    except:
        disconnect_from_wifi()
        print('Could not connect to network')
        return
    
    if ip is None:
        return

    sock = build_socket_tcp(ip, port)

    sock.listen(1)
    print(f'Socket ready, IP: {ip}')

    return sock