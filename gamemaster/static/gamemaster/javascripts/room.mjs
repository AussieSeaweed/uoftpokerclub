class Room {
    updatedOn = null;
    user = null;
    seats = [];
    context = null;
    actions = [];

    constructor() {
        this.socket = new WebSocket(getWebsocketProtocol() + "//" + location.host + location.pathname);
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);

            this.updatedOn = new Date(data.updated_on);
            this.user = data.user;
            this.seats = data.seats;
            this.context = data.context;
            this.actions = data.actions;

            this.refresh();
        };

        $("#command-online").click(() => this.send("/Online"));
        $("#command-offline").click(() => this.send("/Offline"));
        $("#command-away").click(() => this.send("/Away"));
    }

    get seat() {
        for (let seat of this.seats)
            if (this.user !== null && seat.user !== null && this.user.username === seat.user.username)
                return seat;

        return null;
    }

    get users() {
        const users = [];

        for (let seat of this.seats)
            if (seat.user !== null)
                users.push(seat.user);

        return users;
    }

    send(data) {
        this.socket.send(JSON.stringify(data));
    }

    refresh() {
        this.updateCommands();

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

        if (this.actions.length === 0)
            this.clearActions();
        else
            this.updateActions();
    }

    updateCommands() {
        if ((this.seat === null && this.seats.length !== this.users.length) ||
            (this.seat !== null && this.seat.status !== "Online"))
            $("#command-online").show();
        else
            $("#command-online").hide();

        if (this.seat !== null && this.seat.status === "Online") {
            $("#command-offline").show();
            $("#command-away").show();
        } else if (this.seat !== null && this.seat.status === "Away") {
            $("#command-offline").show();
            $("#command-away").hide();
        } else {
            $("#command-offline").hide();
            $("#command-away").hide();
        }
    }


    updateSeat(i) {
        $(`#seat-${i}-wrapper`).click(() => open(this.seats[i].user.profile.url));
        $(`#seat-${i}-avatar`).attr("src", this.seats[i].user.profile.gravatar_url);
        $(`#seat-${i}-username`).text(this.seats[i].user.username);
        $(`#seat-${i}-status`).text(this.seats[i].status === "Online" ? null : this.seats[i].status);

        if (this.seats[i].player === null)
            this.clearPlayer(i);
        else
            this.updatePlayer(i);
    }

    clearSeat(i) {
        $(`#seat-${i}-wrapper`).click(null);
        $(`#seat-${i}-avatar`).attr("src", "/static/images/transparent.png");
        $(`#seat-${i}-username`).text(null);
        $(`#seat-${i}-status`).text(null);

        this.clearPlayer(i);
    }

    updatePlayer(i) {

    }

    clearPlayer(i) {
        $(`#seat-${i}-progress-bar`).css("width", 0);
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
