import socket

def build_socket(ip='0.0.0.0', port=8080):

    print(f'Building socket on IP: {ip} , Port: {port}')
    address = socket.getaddrinfo(ip, port)[0][-1]

    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Releases port on restart/crash
    sock.bind(address)

    return sock