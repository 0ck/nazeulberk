$(document).ready(function(){
  var ws;
  // Connect to Web Socket
  var mj = false;
  ws = new WebSocket("ws://localhost:13254/");

  function init_player(){
    var id_perso = $('#id_perso').val();
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
    if(data == "" || data == '[]')
      return;
    if(is_Json(data)){
      if(JSON.parse(data)['type'] == "isGameMaster")
        if(JSON.parse(data)['value'] == "true")
          mj = true

      generatePlayerList(data);
      console.log(data);
      return;
    }
    output("Message recu : " + e.data);
    
    
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

$('.playerlist_editor_container').on('click', '#saveStats', function() {
  if(!mj)
    return;

    var id_client = $(this).attr('data-id');
    var cou = $('#cou'+id_client).val();
    var cha = $('#cha'+id_client).val();
    var ad = $('#ad'+id_client).val();
    var intel = $('#int' + id_client).val();
    var fo = $('#fo' + id_client).val();
    var pvmax = $('#pvmax' + id_client).val();
    var pv = $('#pv' + id_client).val();
    var pmmax = $('#pmmax' + id_client).val();
    var pm = $('#pm' + id_client).val();
    var att = $('#att' + id_client).val();
    var prd = $('#prd' + id_client).val();
    var destin = $('#destin' + id_client).val();
    var po = $('#po' + id_client).val();

    var prepareStats = {
      'type' : "stats_Change",
      'id_client' : id_client,
      'cou' : cou,
      'cha' : cha,
      'ad' : ad,
      'intel' : intel,
      'fo' : fo,
      'pvmax' : pvmax,
      'pv' : pv,
      'pmmax': pmmax,
      'pm' : pm,
      'att' : att,
      'prd' : prd,
      'destin' : destin,
      'po' : po
    }
    data = JSON.stringify(prepareStats);
    console.log(data);
    ws.send(data);
});

  $(document).keyup(function (e) {
    if (e.keyCode == 13) {
        send_Message();
    }
    if (e.keyCode == 65) {
        isMJ();
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

  function isMJ(){
    ws.send("/mz");
  }
 
  function output(str) {
   
      $('.chatbox_container').html($('.chatbox_container').html() + "<p>"+ str +"</p>");
      $("#chatbox_container").scrollTop($("#chatbox_container")[0].scrollHeight);
  }
  
  function generatePlayerList(data)
  {
    generateMJTools(data);
    data[data.length] = "";
    data[0] = "";
    data = JSON.parse(data);
    $('.playerlist_container').html('');
    data.forEach(function(entry){
      var carac = entry['carac'];
      var perso = entry['perso'];
      var name = perso[1];
      console.log(name);
      $('.playerlist_container').append('<div class="col-lg-3">'+ name + '<img src="#.jpg" width="100%" height="100px"/><div class="progress"><div class="progress-bar" style="width:50%; background-color: red" aria-valuemax="100" aria-valuemin="0" aria-valuenow="50" role="progressbar"><span>' + carac[0] + '</span></div></div></div>');
    });
  }

    function generateMJTools(data){
   
    data[data.length] = "";
    data[0] = "";
    data = JSON.parse(data);
    $('.playerlist_editor_container').html('');
    data.forEach(function(entry){
      var carac = entry['carac'];
      var perso = entry['perso'];
      var name = perso[1];
      console.log("ID WEBSOCKET = " + entry['id']);
      $('.playerlist_editor_container').append('&nbsp;&nbsp;&nbsp;' + perso[1] + '<br /><a class="btn btn-success" data-toggle="modal" data-target="#basicModal' +  entry['id'] + '">Editer fiche personnage</a><br /><br /><div class="modal fade" id="basicModal' + entry['id'] + '" tabindex="-1" role="dialog" aria-labelledby="basicModal" aria-hidden="true"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">x</button><h4 class="modal-title" id="myModalLabel">Fiche personnage : ' + name + ' </h4></div><ul><li></span>Cou : <input id="cou' + entry['id'] + '" type="text" value="' + carac[0] + '"/></li><li></span>Cha : <input id="cha' + entry['id'] + '" type="text" value="' + carac[1]+ '"/></li><li></span>Ad : <input id="ad' + entry['id'] + '" type="text" value="' + carac[2] + '"/></li><li></span>Int : <input id="int' + entry['id'] + '" type="text" value="' + carac[3] + '"/></li><li></span>Fo : <input id="fo' + entry['id'] + '" type="text" value="' + carac[4] + '"/></li><li></span>PV max : <input id="pvmax' + entry['id'] + '" type="text" value="' + carac[5] + '"/></li><li></span>Pv : <input id="pv' + entry['id'] + '" type="text" value="' + carac[6]+ '"/></li><li></span>PM max : <input id="pmmax' + entry['id'] + '" type="text" value="' + carac[7] + '"/></li><li></span>PM : <input id="pm' + entry['id'] + '" type="text" value="' + carac[8]+ '"/></li><li></span>Att : <input id="att' + entry['id'] + '" type="text" value="' + carac[9] + '"/></li><li></span>Prd : <input id="prd' + entry['id'] + '" type="text" value="' + carac[10] + '"/></li><li></span>Point du destin : <input id="destin' + entry['id'] + '" type="text" value="' + carac[11] + '"/></li><li></span>Pieces dor : <input id="po' + entry['id'] + '" type="text" value="' + carac[12] + '"/></li></ul><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">Close</button><button type="button" class="btn btn-primary" id="saveStats" data-id="' + entry['id'] + '">Save changes</button></div></div></div></div>');
    });

    }

    function checkType(data)
    {
      //console.log(data);
      data[data.length] = "";
      data[0] = "";
      data = JSON.parse(data);
      for (var prop in data) {
        if(prop == "type"){
          return data[prop];
        }
      }
        
    }


  function is_Json(string){
    if(string[0] == "[" || string[0] == "{"){
      return true;
      
    }
    return false;
  };
});