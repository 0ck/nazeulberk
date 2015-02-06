var locationws = location.href.replace('http', 'ws').replace(':5000/', ':8765/')
var ice_serv = {"iceServers": [{"url": "stun:stun.l.google.com:19302"}]};
var ws = new WebSocket(locationws);
var pc;

ws.sync_send = function(txt) {
    if (ws.readyState === 1)
    {
        ws.send(txt);
        return;
    }
    setTimeout(function() {
        ws.sync_send(txt);
    }, 3);
};

// call start() to initiate
function start() {
    console.log("START");
    pc = new RTCPeerConnection(ice_serv);

    // send any ice candidates to the other peer
    pc.onicecandidate = function (evt) {
        console.log("ON ICE");
        if (evt.candidate)
        {
            txt = JSON.stringify({ "candidate": evt.candidate });
            console.log(txt);
            console.log("WS: " + ws);
            ws.sync_send(txt);
        }
    };

    // let the "negotiationneeded" event trigger offer generation
    pc.onnegotiationneeded = function () {
        console.log("NEGO NEEDED");
        pc.createOffer(localDescCreated, logError);
    }

    // once remote stream arrives, show it in the remote video element
    pc.onaddstream = function (evt) {
        console.log("RCV STREAM???");
        //.src = URL.createObjectURL(evt.stream);
    };

    // get a local stream, show it in a self-view and add it to be sent
    getUserMedia({ "audio": true, "video": true }, function (stream) {
        console.log("SEND STREAM");
        var selfView = document.getElementById("local");
        selfView.src = URL.createObjectURL(stream);
        pc.addStream(stream);
        pc.onnegotiationneeded();
    }, logError);
}

function localDescCreated(desc) {
    console.log("LOCAL DESC");
    pc.setLocalDescription(desc, function () {
        console.log("SET LOCAL DESC & SEND");
        txt = JSON.stringify({ "sdp": pc.localDescription });
        console.log(txt);
        console.log("WS: " + ws);
        ws.sync_send(txt);
    }, logError);
}

ws.onmessage = function (evt) {
    console.log("LOCAL DESC");
    if (!pc)
        start();

    var message = JSON.parse(evt.data);
    if (message.sdp)
        pc.setRemoteDescription(new RTCSessionDescription(message.sdp), function () {
            console.log("SET REMOTE DESC");
            // if we received an offer, we need to answer
            if (pc.remoteDescription.type == "offer")
                pc.createAnswer(localDescCreated, logError);
        }, logError);
    else
    {
        console.log("ADD ICE");
        pc.addIceCandidate(new RTCIceCandidate(message.candidate), logError);
    }
};

function logError(error) {
    log(error.name + ": " + error.message);
}

start();

//var initiator;
//
//function initiatorCtrl(event) {
//    console.log("INIT CTRL");
//    console.log(event.data);
//    if (event.data == "fullhouse") {
//        alert("full house");
//    }
//    if (event.data == "initiator") {
//        initiator = false;
//        init();
//    }
//    if (event.data == "not initiator") {
//        initiator = true;
//        init();
//    }
//}
//
//ws.onmessage = initiatorCtrl;
//function init() {
//    console.log("INIT");
//    var constraints = {
//        audio: true,
//        video: true
//    };
//    getUserMedia(constraints, connect, fail);
//}
//
//function connect(stream) {
//    console.log("CONNECT");
//    var localV = document.getElementById("local");
////    var remoteV = document.getElementById("remote");
//    pc = new RTCPeerConnection(ice_serv);
//    if (stream) {
//        console.log("STREAM");
//        pc.addStream(stream);
//        localV.src = URL.createObjectURL(stream);
//        console.log("LOCAL:" + localV.src)
//        localV.play();
//    }
//    /*
//    pc.onaddstream = function(event) {
//        remoteV.src = URL.createObjectURL(stream);
//        console.log("REMOTE:" + remoteV.src)
//        remoteV.play();
//        logStreaming(true);
//    };*/
//    pc.onicecandidate = function(event) {
//        console.log("ON ICE");
//        if (event.candidate) {
//            console.log("ICE:" + event.candidate)
//            ws.send(JSON.stringify(event.candidate));
//        }
//    };
//    ws.onmessage = function (event) {
//        console.log("ON MESSAGE");
//        var signal = JSON.parse(event.data);
//        if (signal.sdp) {
//            if (initiator) {
//                receiveAnswer(signal);
//            } else {
//                receiveOffer(signal);
//            }
//        } else if (signal.candidate) {
//            console.log("ADD ICE");
//            pc.addIceCandidate(new RTCIceCandidate(signal));
//        }
//    };
//    if (initiator) {
//        createOffer();
//    } else {
//        log('waiting for offer...');
//    }
//    logStreaming(false);
//}
//
//function createOffer() {
//    log('creating offer...');
//    pc.createOffer(function(offer) {
//        log('created offer...');
//        pc.setLocalDescription(offer, function() {
//        log('sending to remote...');
//        ws.send(JSON.stringify(offer));
//        }, fail);
//    }, fail);
//}
//
//function receiveOffer(offer) {
//    log('received offer...');
//    pc.setRemoteDescription(new RTCSessionDescription(offer), function() {
//        log('creating answer...');
//        pc.createAnswer(function(answer) {
//            log('created answer...');
//            pc.setLocalDescription(answer, function() {
//                log('sent answer');
//                ws.send(JSON.stringify(answer));
//            }, fail);
//        }, fail);
//    }, fail);
//}
//
//function receiveAnswer(answer) {
//    log('received answer');
//    pc.setRemoteDescription(new RTCSessionDescription(answer));
//}
//
//function log() {
//    var state = document.getElementById("status");
//    state.text += (Array.prototype.join.call(arguments, ' '));
//    console.log.apply(console, arguments);
//}
//
//function logStreaming(streaming) {
//    var stream = document.getElementById("streaming");
//    stream.text += (streaming ? '[streaming]' : '[..]');
//}
//
//function fail() {
//    var state = document.getElementById("status");
//    state.text(Array.prototype.join.call(arguments, ' '));
//    state.addClass('error');
//    console.error.apply(console, arguments);
//}
//
