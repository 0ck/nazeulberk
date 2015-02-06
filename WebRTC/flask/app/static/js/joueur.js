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
        console.log("ON ICE: " + evt);
        if (evt.candidate)
        {
            txt = JSON.stringify({ "candidate": evt.candidate });
            console.log(txt);
            console.log("WS: " + ws);
            ws.sync_send(txt);
            console.log("SENT");
        }
    };

    // let the "negotiationneeded" event trigger offer generation
    pc.onnegotiationneeded = function () {
        console.log("NEGO NEEDED");
        pc.createOffer(localDescCreated, logError);
    }

    // once remote stream arrives, show it in the remote video element
    pc.onaddstream = function (evt) {
        var remoteView = document.getElementById("remote");
        remoteView.src = URL.createObjectURL(evt.stream);
    };

    pc.createDataChannel({});
    pc.onnegotiationneeded();
}

function localDescCreated(desc) {
    console.log("LOCAL DESC");
    pc.setLocalDescription(desc, function () {
        console.log("SET LOCAL DESC & SEND");
        txt = JSON.stringify({ "sdp": pc.localDescription });
        console.log(txt)
        console.log("WS: " + ws);
        ws.sync_send(txt);
        console.log("SENDED");
    }, logError);
}

ws.onmessage = function (evt) {
    console.log("ON MESSAGE!!!");
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
    else if (message.candidate)
    {
        console.log("ADD ICE");
        pc.addIceCandidate(new RTCIceCandidate(message.candidate), logError);
    }
    else
    {
        console.log("RECU " + message);
    }
};

function logError(error) {
    console.log(error.name + ": " + error.message);
}

start();
