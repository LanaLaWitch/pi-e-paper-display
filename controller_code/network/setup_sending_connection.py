import socket
from shared.config import TCP_PORT

def establish_sending_connection():
    ip = _get_ip()
    return connect_to_display_port(ip)

def _get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def connect_to_display_port(ip, port=TCP_PORT):

    print(f'Connecting to display at {ip}:{port}')
    address = socket.getaddrinfo(ip, port)[0][-1]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    response = sock.recv(16)
    if response != b'READY':
        sock.close()
        raise ConnectionError(f'Unexpected response from display: {response}')

    print('Connected to display')
    return sock
