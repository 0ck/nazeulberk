from py.room.websocket import WebSocketsServer
from array import array
import random
from flask import session
import json
#DATBASE LINK
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
#Database connect
engine = create_engine('sqlite:///naheul.db')
dbSession = Session(engine)

clients = {}
rooms = []
  # Called for every client connecting (after handshake)
def new_client(client, server):
  print("Un nouveau client arrive sur le serveur IDENTIFIANT -> %d" % client['id'])
  clients[client['id']] = [client, 0] # 155 = room ID
  #print(clients)
  server.send_message_to_all("<span style='color: red'>Le client  arrive sur le serveur  -></span> %d" % client['id'])


def client_left(client, server):
  print("client disconnected")
  left_channel(client, server)
  del clients[client['id']]
  

  # Called when a client sends a message
def message_received(client, server, message):
  if(is_json(message)):
    data = json.loads(message)
    print(data['type'])
    print('its a json')
    if(data['type'] == "stats_Change"):
      change_stats(client, data)
    return
  #print("Client said: %s" % (message))
  if(isCommand(client, server, message)):
    return
  message_to_room(client, server, "Client said: %s" % (message))


def message_to_room(client, server, message):
  for i in clients:
    if(clients[i][1] == get_client_room(client)):
      #print(clients[i][1])
      #print(get_client_room(client))
      server.send_message(clients[i][0], message)

def get_client_room(client):
  for i in clients:
    if(clients[i][0]['id'] == client['id']):
      return clients[i][1]

def isCommand(client, server, message):
  if(len(message) > 0):
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
    create_room(client, commandName[1], server, commandName[2])
  if(commandName[0] == "/list_all_rooms"):
    list_all_rooms(client, server)
  if(commandName[0] == "/join_channel"):
    join_channel(client, server, commandName[1])
  if(commandName[0] == "/select_hero"):
    init_player(client, commandName[1])
  if(commandName[0] == "/mj"):
    isGameMaster(client, server)
  if(commandName[0] == "/mz"):
    MJ_TOOL(client, server, clients[client['id']][1])
    #list_player(client, server, clients[client['id']][1])

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
    #message_to_room(client, server, "<span style='color: red'>Client(%d) fait un jet de D, résultat -> %d</span>" % (client['id'], randomInt)) 
  # else:
  #   server.send_message(client, "<span style='color:red'> Veuillez utiliser la syntaxe '/roll nb_dès D*puissance_des_dès*' exemple pour un 8 jet de dès à 6 faces : /roll 8 D6</span>")

def create_room(client, name, server, slot=1):
  new_index = get_index_maxroom() + 1
  new_room = {'id': new_index, 'name' : name, 'slot' : slot, 'clientsID' : [], 'mj' : ''}
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
  #print(rooms)
  server.send_message(client, json.dumps(rooms))

def join_channel(client, server,  id):
  id = int(id)
  clients[client['id']][1] = id
  for i in rooms:
    if(id == i['id']):
      if(i['mj'] == ''):
        i['mj'] = client['id']
      else:
        i['slot'] = str(int(i['slot']) - 1)
        i['clientsID'].append(client['id'])

  list_player(client, server, id)
  # rooms[id]['clientsID'].append(client['id'])
  #print(rooms)

def left_channel(client, server):
  for i in rooms:
    if(client['id'] == i['mj']):
      i['mj'] = ''
    print(rooms)
    for test in i['clientsID']:
      if(test == client['id']):
          i['clientsID'].remove(client['id'])
          i['slot'] = str(int(i['slot']) + 1)
          list_player(client, server, i['id'])
          



#############################
###                         #
###       GAMEPLAY          #
###                         #
#############################
def init_player(client, id_perso):
  persoJoueur = engine.execute('SELECT * FROM Avatar WHERE id = ' + id_perso).first()
  caracs = engine.execute('SELECT * FROM Carac WHERE id = ' + id_perso).first()
  clients[client['id']].append(prepareJson(persoJoueur))
  clients[client['id']].append(prepareJson(caracs))
  #print(clients[client['id']][3]['AD'])

def list_player(client, server, id_room):
  tab = []
  count = 0
  print (id_room)
  for i in rooms:
    if(i['id'] == id_room):
      for x in i['clientsID']:
        print(x)
        personnage = clients[x][2]
        carac = clients[x][3]
        print(carac)
        tab.append({'type' : 'list_player', 'carac' : carac, 'perso' : personnage, 'id' : x})
        #count = count + 1
  message_to_room(client, server, json.dumps(tab))

def MJ_TOOL(client, server, id_room):
  if(isGameMaster(client, server) == 0):
    return

  tab = []
  count = 0
  for i in rooms:
    if(i['id'] == id_room):
      for x in i['clientsID']:
        print(x)
        personnage = clients[x][2]
        carac = clients[x][3]
        tab.append({'carac' : carac, 'perso' : personnage, 'id' : x})
        #count = count + 1
  server.send_message(client, json.dumps(tab))

def prepareJson(array):
  data = []
  count = 0
  for perso in array:
    data.append(perso)
    count = count + 1

  return data


def isGameMaster(client, server):
  room_id = get_client_room(client)
  print(rooms)
  for i in rooms:
    if(i['id'] == room_id):
      if(client['id'] == i['mj']):
        server.send_message(client, json.dumps({'type' : 'isGameMaster', 'value' : 'true'}))
        return 1

  server.send_message(client, json.dumps({'type' : 'isGameMaster', 'value' : 'false'}))
  return 0

def is_json(message):
  if(message[0] == '[' or message[0] == '{'):
    return 1
  return 0

def change_stats(client, data):
  id_client = int(data['id_client'])
  clients[id_client][3][0] = data['cou']
  clients[id_client][3][1] = data['cha']
  clients[id_client][3][2] = data['ad']
  clients[id_client][3][3] = data['intel']
  clients[id_client][3][4] = data['fo']
  clients[id_client][3][5] = data['pvmax']
  clients[id_client][3][6] = data['pv']
  clients[id_client][3][7] = data['pmmax']
  clients[id_client][3][8] = data['pm']
  clients[id_client][3][9] = data['att']
  clients[id_client][3][10] = data['prd']
  clients[id_client][3][11] = data['destin']
  clients[id_client][3][12] = data['po']
  print('before')
  print(clients[id_client][3][0])
  list_player(client, server, clients[client['id']][1])


PORT=13254
server = WebSocketsServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
