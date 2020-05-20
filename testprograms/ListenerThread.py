#!/usr/bin/env python3

import threading


class ListenerThread(threading.Thread):

    def __init__(self, client):
        threading.Thread.__init__(self, daemon=True)

        self.client = client


    def run(self):
        print("Starting listening thread")

        while True:
            raw = self.client.recv(1024)

            if raw:
                data = str(raw)
                # data = data[2:-1]

                # print("Received: ", data)

                print(data)
