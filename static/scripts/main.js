function createWebSocketURL(websocketPath) {
    return (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + websocketPath;
}

function main() {
    const canvases = document.getElementsByTagName('canvas');

    for (let canvas of canvases)
        games.push(new gameTypes[canvas.getAttribute('data-game-name')](
            canvas.getContext('2d'),
            createWebSocketURL(canvas.getAttribute('data-websocket-path'))),
        );
}

const gameTypes = {
    'Tic Tac Toe': TicTacToeRoom,
}, games = [];

main();
