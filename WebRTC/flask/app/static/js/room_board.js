$(document).ready(function(){
  var ws;
  var jsonList = ""
  // Connect to Web Socket
  ws = new WebSocket("ws://localhost:13254/");
 
  // Set event handlers.
  ws.onopen = function() {
    output("Un nouveau client à rejoint la salle");
    ws.send("/list_all_rooms");
  };
 
  ws.onmessage = function(e) {
    // e.data contains received string.
    console.log(e.data);
    output("Message recu : " + e.data);
    jsonList = e.data;
    console.log(JSON.parse(jsonList));
    generateRoomList();
  };
 
  ws.onclose = function() {
    output("Connexion au serveur fermé");
  };
 
  ws.onerror = function(e) {
    output("Une erreur a été rencontré");
    console.log(e)
  };
  function output(str) {
    console.log(str);
  }

  function generateRoomList(){
    
    var json = JSON.parse(jsonList);
    var name = $('#room_name');
    
    console.log(jsonList);
    $('tbody').html();
    json.forEach(function(entry){
      var name = entry.name;
      var id = entry.id;
      var slot = entry.slot;
      if(slot > 0){
        $('tbody').html($('tbody').html() + "<tr><td>" + id + "</td><td>Salle "+ name + "</td><td>" + entry.slot +" Places</td><td><a href='/room/"+ id +"'>Rejoindre</a></td></tr>");
      }
      
    });
    setTimeout(generateRoomList, 30000);
  }

  $('#create_room').click(function(){
    var name = $('#party_name').val();
    var slot = $('#NBslot').val();
    console.log(slot);
    ws.send("/create_room "+ name + " " + slot);
  });
 
});