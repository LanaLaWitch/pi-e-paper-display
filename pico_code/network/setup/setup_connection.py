def start_server_tcp(ip, port):
    from shared.network.socket_handler import build_socket_tcp

    sock = build_socket_tcp(ip, port)

    sock.listen(1)
    print(f'TCP socket ready, IP: {ip}')

    return sock

def start_server_udp(ip, port):
    from shared.network.socket_handler import build_socket_udp

    sock = build_socket_udp(ip, port)

    sock.listen(1)
    print(f'UDP socket ready, IP: {ip}')

    return sock