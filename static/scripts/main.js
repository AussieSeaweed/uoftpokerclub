function createWebsocketUrl(websocketPath) {
    return (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + websocketPath; // TODO: TEST WITHOUT PROTOCOL AND HOST
}