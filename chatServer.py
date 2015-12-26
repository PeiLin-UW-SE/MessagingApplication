import socket

database = []

state = True


def server():
    global state
    host = "127.0.0.1"
    port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print("----- SERVER IS ON-----")

    while state:
        encoded_data, address = s.recvfrom(1024)
        decoded_data = encoded_data.decode("utf-8")

        if address not in database:
            database.append(address)

        if "SHUTDOWN" in decoded_data:
            print("----- SERVER IS OFF -----")
            state = False
        else:
            print("Received From: " + str(address) + "\n    " + str(decoded_data))
            for client in database:
                s.sendto(encoded_data, client)
    s.close()

if __name__ == '__main__':
    server()
