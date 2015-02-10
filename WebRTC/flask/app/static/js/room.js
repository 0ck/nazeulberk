var locationws = location.href.replace('http', 'ws').replace(':5000/', ':8765/')
var ws = new WebSocket(locationws);
var initiator;
var pc;

function initiatorCtrl(event) {
    console.log("INIT CTRL");
    console.log(event.data);
    if (event.data == "fullhouse") {
        alert("full house");
    }
    if (event.data == '{"initiator": true}') {
        initiator = false;
        init();
    }
    if (event.data == '{"initiator": false}') {
        initiator = true;
        init();
    }
}

ws.onmessage = initiatorCtrl;
function init() {
    var constraints = {
        audio: true,
        video: true
    };
    getUserMedia(constraints, connect, fail);
}

function connect(stream) {
    var localV = document.getElementById("local");
    var remoteV = document.getElementById("remote");
    pc = new RTCPeerConnection(null);
    if (stream) {
        pc.addStream(stream);
        localV.src = URL.createObjectURL(stream);
        console.log("LOCAL:" + localV.src)
        localV.play();
    }
    pc.onaddstream = function(event) {
        remoteV.src = URL.createObjectURL(stream);
        console.log("REMOTE:" + remoteV.src)
        remoteV.play();
        logStreaming(true);
    };
    pc.onicecandidate = function(event) {
        if (event.candidate) {
            console.log("ICE:" + event.candidate)
            ws.send(JSON.stringify(event.candidate));
        }
    };
    ws.onmessage = function (event) {
        var signal = JSON.parse(event.data);
        if (signal.sdp) {
            if (initiator) {
                receiveAnswer(signal);
            } else {
                receiveOffer(signal);
            }
        } else if (signal.candidate) {
            pc.addIceCandidate(new RTCIceCandidate(signal), function(){}, fail);
        }
    };
    if (initiator) {
        createOffer();
    } else {
        log('waiting for offer...');
    }
    logStreaming(false);
}

function createOffer() {
    log('creating offer...');
    pc.createOffer(function(offer) {
        log('created offer...');
        pc.setLocalDescription(offer, function() {
        log('sending to remote...');
        ws.send(JSON.stringify(offer));
        }, fail);
    }, fail);
}

function receiveOffer(offer) {
    log('received offer...');
    pc.setRemoteDescription(new RTCSessionDescription(offer), function() {
        log('creating answer...');
        pc.createAnswer(function(answer) {
            log('created answer...');
            pc.setLocalDescription(answer, function() {
                log('sent answer');
                ws.send(JSON.stringify(answer));
            }, fail);
        }, fail);
    }, fail);
}

function receiveAnswer(answer) {
    log('received answer');
    pc.setRemoteDescription(new RTCSessionDescription(answer), function() {}, fail);
}

function log() {
    //var state = document.getElementById("status");
    //state.text += (Array.prototype.join.call(arguments, ' '));
    console.error.apply(console, arguments);
}

function logStreaming(streaming) {
    var stream = document.getElementById("streaming");
    stream.text += (streaming ? '[streaming]' : '[..]');
}

function fail() {
    //var state = document.getElementById("status");
    //state.text(Array.prototype.join.call(arguments, ' '));
    //state.addClass('error');
    console.error.apply(console, arguments);
}