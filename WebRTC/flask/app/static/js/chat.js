$(document).ready(function(){
  var ws;
  // Connect to Web Socket
  ws = new WebSocket("ws://localhost:13254/");

  function init_player(){
    var id_perso = $('#persoID').val();
    ws.send("/select_hero "+ id_perso);
  }
  // Set event handlers.
  ws.onopen = function() {
    init_player();
    ws.send('/join_channel ' + $('#room_id').val())
    output("<span style='color: green'>[CONSOLE]</span> Un nouveau client à rejoint la salle");
  };
 
  ws.onmessage = function(e) {
    var data = e.data;
    // e.data contains received string.
    type = data[0]['type'];

    output("Message recu : " + e.data);
    
    generatePlayerList(data);
  };
 
  ws.onclose = function() {
    output("Connexion au serveur fermé");
  };
 
  ws.onerror = function(e) {
    output("Une erreur a été rencontré");
    console.log(e)
  };
 
 
  function onSubmit() {
    var input = document.getElementById("text_value");
    // You can send message to the Web Socket using ws.send.
    output(input.value);
    input.value = "";
    input.focus();
  }
 
  $('#btn_send').click(function(){
    send_Message();
  });

  $('#video_call').click(function(){
    init();
  });
 
  $(document).keyup(function (e) {
    if (e.keyCode == 13) {
        send_Message();
    }
    if (e.keyCode == 65) {
        generatePlayerList();
    }
});
 
  function send_Message(){
    ws.send($('#text_value').val());
    $('#text_value').val("");
    $('#text_value').focus();
  }
 
  function onCloseClick() {
    ws.close();
  }
 
  function output(str) {
    $('.chatbox_container').html($('.chatbox_container').html() + "<p>"+ str +"</p>");
  }
  
  function generatePlayerList(data)
  {
    console.log(data);
    data[data.length] = "";
    data[0] = "";
    console.log(data);
    data = JSON.parse(data);
    console.log(data);
    $('.playerlist_container').html('');
    data.forEach(function(entry){
      var carac = entry['carac'];
      var perso = entry['perso'];
      var name = perso[1];
      console.log(name);
      $('.playerlist_container').append('<div class="col-lg-3" style="padding: 20px"><div class="elem"><img src="azdeqs.jpg" width="100%" height="100px"/>'+ name +'<div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="70"aria-valuemin="0" aria-valuemax="100" style="width:70%; background-color: red"><span >20/30 HP</span></div></div></div>');
    });
  }
});