class Room {
    user = null;
    seats = [];
    context = null;
    actions = null;

    constructor() {
        this.socket = new WebSocket(getWebsocketProtocol() + "//" + window.location.host + window.location.pathname);
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);

            this.user = data.user;
            this.seats = data.seats;
            this.context = data.context;
            this.actions = data.actions;

            this.refresh();
        };
    }

    send(data) {
        this.socket.send(JSON.stringify(data));
    }

    refresh() {
        for (let i = 0; i < this.seats.length; ++i) {
            if (this.seats[i].user === null)
                this.clearSeat(i);
            else
                this.updateSeat(i);
        }

        if (this.context === null)
            this.clearContext();
        else
            this.updateContext();

        if (this.actions === null)
            this.clearActions();
        else
            this.updateActions();
    }

    updateSeat(i) {
        $(`#seat-${i}-wrapper`).click(() => window.open(this.seats[i].user.profile.url));
        $(`#seat-${i}-avatar`).attr("src", this.seats[i].user.profile.gravatar_url);
        $(`#seat-${i}-username`).text(this.seats[i].user.username);
    }

    clearSeat(i) {
        $(`#seat-${i}-wrapper`).click(() => {
        });
        $(`#seat-${i}-avatar`).attr("/static/images/transparent.png");
        $(`#seat-${i}-username`).text(null);
    }

    updateContext() {

    }

    clearContext() {

    }

    updateActions() {

    }

    clearActions() {

    }
}

export {Room};
