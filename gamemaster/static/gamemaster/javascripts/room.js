class Room {
    user = null;
    updated_on = null;
    timeout = null;
    config = {};
    seats = [];
    context = null;
    actions = [];

    constructor() {
        $("#toggle-connect").click(() => this.send(null));
        $("#toggle-disconnect").click(() => this.send(null));

        this.connect();

        setTimeout(() => {
            $("#game").animate({opacity: 1});
            $("#toggle").animate({opacity: 1});
        }, 400);
    }

    get seat() {
        if (this.user !== null)
            for (let seat of this.seats)
                if (seat.user !== null && this.user.username === seat.user.username)
                    return seat;

        return null;
    }

    get users() {
        return this.seats.filter(seat => seat.user !== null).map(seat => seat.user);
    }

    get players() {
        return this.seats.filter(seat => seat.player !== null).map(seat => seat.player);
    }

    connect() {
        this.socket = new WebSocket(getWebsocketProtocol() + "//" + location.host + location.pathname);

        this.socket.onmessage = event => {
            const data = JSON.parse(event.data);

            this.user = data.user;
            this.updated_on = new Date(data.updated_on);
            this.timeout = data.timeout * 1000;
            this.config = data.config;
            this.seats = data.seats;
            this.context = data.context;
            this.actions = data.actions;

            this.refresh();
        };

        this.socket.onclose = event => setTimeout(this.connect());
    }

    send(data) {
        this.socket.send(JSON.stringify(data));
    }

    refresh() {
        this.updateTogglers();

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

    updateTogglers() {
        if ((this.seat === null && this.seats.length !== this.users.length) ||
            (this.seat !== null && !this.seat.status))
            $("#toggle-connect").show();
        else
            $("#toggle-connect").hide();

        if (this.seat !== null && this.seat.status)
            $("#toggle-disconnect").show();
        else
            $("#toggle-disconnect").hide();
    }

    updateSeat(i) {
        $(`#seat-${i}`).finish().animate({opacity: 1});
        $(`#seat-${i}-tag`).off("click")
            .on("click", () => open(this.seats[i].user.profile.url))
            .attr("data-status", this.seats[i].status)
            .attr("data-original-title", this.seats[i].stats.join("<br/>"));

        $(`#seat-${i}-avatar`).attr("src", this.seats[i].user.profile.gravatar_url);
        $(`#seat-${i}-username`).text(this.seats[i].user.username);
        $(`#seat-${i}-status`).text(this.seats[i].status ? null : "Away");

        if (this.seats[i].player === null)
            this.clearPlayer(i);
        else
            this.updatePlayer(i);
    }

    clearSeat(i) {
        $(`#seat-${i}`).finish().animate({opacity: 0});
        $(`#seat-${i}-tag`).off("click")
            .attr("data-status", "")
            .attr("data-original-title", "")
            .tooltip("hide");

        $(`#seat-${i}-avatar`).attr("src", "/static/gamemaster/images/transparent.png");
        $(`#seat-${i}-username`).text(null);
        $(`#seat-${i}-status`).text(null);

        this.clearPlayer(i);
    }

    updatePlayer(i) {

    }

    clearPlayer(i) {
        $(`#seat-${i}-progress-bar`).finish().css("width", 0);
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
