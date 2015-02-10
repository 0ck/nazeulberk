from websocket import WebSocketsServer

# Called for every client connecting (after handshake)
def new_client(client, server):
   print("Un nouveau client arrive sur le serveur IDENTIFIANT -> %d" % client['id'])
   server.send_message_to_all("<span style='color: red'>Un nouveau client arrive sur le serveur IDENTIFIANT -></span> %d" % client['id'])


# Called for every client disconnecting
def client_left(client, server):
   print("Client(%d) disconnected" % client['id'])
   server.send_message_to_all("<span style='color: red'>Client(%d) disconnected</span>" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
   print("Client(%d) said: %s" % (client['id'], message))
   server.send_message_to_all("<span style='color: red'>Client(%d) said: %s </span>" % (client['id'], message))

PORT=13254
server = WebSocketsServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()