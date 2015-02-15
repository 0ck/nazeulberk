from websocket import WebSocketsServer
from array import array
import random
from flask import session
import json
clients = {}
rooms = []
  # Called for every client connecting (after handshake)
def new_client(client, server):
  print("Un nouveau client arrive sur le serveur IDENTIFIANT -> %d" % client['id'])
  clients[client['id']] = [client, 0] # 155 = room ID
  print(clients)
  server.send_message_to_all("<span style='color: red'>Le client  arrive sur le serveur  -></span> %d" % client['id'])


def client_left(client, server):
  print("client disconnected")
  del clients[client['id']]

  # Called when a client sends a message
def message_received(client, server, message):
  print("Client said: %s" % (message))
  if(isCommand(client, server, message)):
    return
  message_to_room(client, server, "Client said: %s" % (message))


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
  if(commandName[0] == "/roll"):
    roll(client, server, commandName[1], commandName[2])
  if(commandName[0] == "/create_room"):
    create_room(client, commandName[1], server)
  if(commandName[0] == "/list_all_rooms"):
    list_all_rooms(client, server)
  if(commandName[0] == "/join_channel"):
    join_channel(client, commandName[1])
  else:
    server.send_message(client, "<span style='color:red'> Cette commande n'existe pas</span>")

def combat_Action(client, server, message):
  message_to_room(client, server, "Lancement d'un combat par le client {%d}" % client['id'])

def roll(client, server, number, value, malus=0):
    number = int(number)
    value = value.split('D')
    value2 = int(value[1])
    minValue = (number)
    MaxValue = (value2 * number)
    randomInt = random.randint(minValue, MaxValue)
    message_to_room(client, server, "%d" % randomInt)
    message_to_room(client, server, "<span style='color: red'>Client(%d) fait un jet de D, résultat -> %d</span>" % (client['id'], randomInt)) 
  # else:
  #   server.send_message(client, "<span style='color:red'> Veuillez utiliser la syntaxe '/roll nb_dès D*puissance_des_dès*' exemple pour un 8 jet de dès à 6 faces : /roll 8 D6</span>")

def create_room(client, name, server, slot=1):
  new_index = get_index_maxroom() + 1
  new_room = {'id': new_index, 'name' : name, 'mj' : client, 'client' : '', 'slot': slot}
  rooms.append(new_room)
  
  #list_all_rooms(client, server)

def delete_room(id_room):
  del rooms[id_room]

def get_index_maxroom():
  count = 0
  for i in rooms:
    count = count + 1
  
  return count

def list_all_rooms(client, server):
  print(rooms)
  server.send_message(client, json.dumps(rooms))

def join_channel(client, id):
  clients[client['id']][1] = id



PORT=13254
server = WebSocketsServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()