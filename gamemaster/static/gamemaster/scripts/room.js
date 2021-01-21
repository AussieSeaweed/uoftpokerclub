function Room() {

}

function SequentialRoom() {

}

function TicTacToeRoom() {

}

function setup() {
    var canvas = document.getElementById(view._id);
    var gameName = canvas.getAttribute('data-game-name');
    var websocketURL = createWebsocketUrl(canvas.getAttribute('data-websocket-path'));
}

var game;
