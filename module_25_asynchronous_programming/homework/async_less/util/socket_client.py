import socket


def run_client():
    address_server = ('127.0.0.1', 8080)
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect(address_server)
    socket_client.sendto(b'Hello world', address_server)
    print(socket_client.recv(1024))
    socket_client.close()


if __name__ == '__main__':
    run_client()
