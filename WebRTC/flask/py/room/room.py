from websocket import WebSocketsServer
from array import array

clients = {}
rooms = []
# Called for every client connecting (after handshake)
def new_client(client, server):
   print("Un nouveau client arrive sur le serveur IDENTIFIANT -> %d" % client['id'])
   clients[client['id']] = [client, 155] # 155 = room ID
   print(clients)
   server.send_message_to_all("<span style='color: red'>Un nouveau client arrive sur le serveur IDENTIFIANT -></span> %d" % client['id'])


# Called for every client disconnecting
def client_left(client, server):
   print("Client(%d) disconnected" % client['id'])
   del clients[client['id']]
   server.send_message_to_all("<span style='color: red'>Client(%d) disconnected</span>" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
	print("Client(%d) said: %s" % (client['id'], message))
	if(isCommand(client, server, message)):
		executeCommand
		return
	message_to_room(client, server, "<span style='color: red'>Client(%d) said: %s </span>" % (client['id'], message))


def message_to_room(client, server, message):
	for i in clients:
		if(clients[i][1] == get_client_room(client)):
			print(clients[i][1])
			print(get_client_room(client))
			server.send_message(clients[i][0], message)

def get_client_room(client):
	for i in clients:
		if(clients[i][0]['id'] == client['id']):
			return clients[i][1]

def isCommand(client, server, message):
	if(message[0] == "/" or message[0] == "!"):
		executeCommand(client, server, message)
		return 1
	return 0

def executeCommand(client, server, message):
	commandName = message.split(' ')
	print(commandName[0])
	if(commandName[0] == "/combat"):
		combat_Action(client, server, message)
	else:
		server.send_message(client, "<span style='color:red'> Cette commande n'existe pas</span>")

def combat_Action(client, server, message):
	message_to_room(client, server, "Lancement d'un combat par le client {%d}" % client['id'])



PORT=13254
server = WebSocketsServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()