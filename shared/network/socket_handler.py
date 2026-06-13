import socket
from shared.config import TCP_PORT, UDP_PORT

def build_socket_tcp(ip='0.0.0.0', port=TCP_PORT):

    print(f'Building socket on IP: {ip} , Port: {port}')
    address = socket.getaddrinfo(ip, port)[0][-1]

    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Releases port on restart/crash
    sock.setblocking(False)
    sock.bind(address)

    return sock

def build_socket_udp(ip='0.0.0.0', port=UDP_PORT):

    print(f'Building socket on IP: {ip} , Port: {port}')
    address = socket.getaddrinfo(ip, port)[0][-1]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Releases port on restart/crash
    sock.setblocking(False)
    sock.bind(address)

    return sock