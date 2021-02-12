class Room {
    constructor(context, webSocketURL) {
        this.context = context;
        this.webSocketURL = webSocketURL;
        this.socket = null;

        this.connect();
        this.setup();
    }

    connect() {
        this.socket = new WebSocket(this.webSocketURL);

        this.socket.onmessage = event => this.update(JSON.parse(event.data));
        this.socket.onclose = () => this.connect(); // TODO: TRY JUST '... = this.connect;'
    }

    setup() {

    }

    update(data) {

    }
}
