import Main
from ev3dev2.connection.ClientSocket import get_client_socket


def main():
    client_socket = get_client_socket()
    client_socket.setup()

    Main.main()


if __name__ == "__main__":
    main()
