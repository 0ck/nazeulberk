#!/usr/bin/env python3
import asyncio
import websockets
import re

path_assoc = dict()
repath = re.compile('/[^/]+/(\d+)')

@asyncio.coroutine
def hello(ws, txtpath):
    global path_assoc
    global repath
    path = repath.search(txtpath).group(1)
    print("RECEIVE {} MSG {}!".format(id(ws), path))
    msg = "not initiator"
    initiator = False
    if path not in path_assoc:
        msg = "initiator"
        initiator = True
        path_assoc[path] = list()
    path_assoc[path].append(ws)
    print("IS {}".format(msg))
    #yield from ws.send(msg)
    message = ""
    # Receive Handler
    while True:
        # check for deconnection
        if not ws.open:
            path_assoc[path].remove(ws)
            if len(path_assoc[path]) == 0:
                del path_assoc[path]
            break
        if msg == "initiator":
            yield from ws.send('{"initiator": true}')
        else:
            yield from ws.send('{"initiator": false}')
        message += yield from ws.recv()
        if message is None:
            break
        sent = 0
        for client in path_assoc[path]:
            # je n'envoie pas a la WS
            if id(client) != id(ws):
                if not client.open:
                    path_assoc[path].remove(client)
                    if len(path_assoc[path]) == 0:
                        del path_assoc[path]
                    continue
                print("EMIT {} to {}:\n{}".format(id(client), id(ws), message))
                yield from client.send(message)
                print("SENDED:" + repr(client))
                sent += 1
        if sent != 0:
            message = ""

start_server = websockets.serve(hello, 'localhost', 8765)

if __name__ == '__main__':
    print("Running Signalling SERVER!")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
