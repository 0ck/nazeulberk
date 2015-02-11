$(document).ready(function(){
  var ws;
  // Connect to Web Socket
  ws = new WebSocket("ws://localhost:13254/");

  // Set event handlers.
  ws.onopen = function() {
    output("<span style='color: green'>[CONSOLE]</span> Un nouveau client à rejoint la salle");
  };

  ws.onmessage = function(e) {
    // e.data contains received string.
    console.log(e.data);
    output("Message recu : " + e.data);
  };

  ws.onclose = function() {
    output("onclose");
  };

  ws.onerror = function(e) {
    output("onerror");
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
    ws.send($('#text_value').val());
  });

  function onCloseClick() {
    ws.close();
  }

  function output(str) {
    $('.chatbox_container').html($('.chatbox_container').html() + "<p>"+ str +"</p>");
  }

});