class Room {
    config = null;
    user = null;
    seats = [];
    context = null;
    actions = [];

    constructor() {
        $("#command-online").click(() => this.send("/Online"));
        $("#command-offline").click(() => this.send("/Offline"));
        $("#command-away").click(() => this.send("/Away"));

        this.connect();

        setTimeout(() => {
            $("#game").animate({opacity: 1});
            $("#command").animate({opacity: 1});
        }, 400);
    }

    /*
        On seat, users, players, and refresh, seat !== null condition is redundant, because the rest framework always
        sends non-null values.
     */

    get seat() {
        if (this.user !== null)
            for (let seat of this.seats)
                if (seat !== null && seat.user !== null && this.user.username === seat.user.username)
                    return seat;

        return null;
    }

    get users() {
        return this.seats.filter(seat => seat !== null && seat.user !== null).map(seat => seat.user);
    }

    get players() {
        return this.seats.filter(seat => seat !== null && seat.player !== null).map(seat => seat.player);
    }

    connect() {
        this.socket = new WebSocket(getWebsocketProtocol() + "//" + location.host + location.pathname);

        this.socket.onmessage = event => {
            const data = JSON.parse(event.data);

            this.config = data.config;
            this.user = data.user;
            this.seats = data.seats;
            this.context = data.context;
            this.actions = data.actions;

            if (this.config) {
                this.config.updated_on = new Date(this.config.updated_on);

                if (this.config.timeout)
                    this.config.timeout *= 1000;
            }

            this.refresh();
        };

        this.socket.onclose = event => this.connect();
    }

    send(data) {
        this.socket.send(JSON.stringify(data));
    }

    refresh() {
        this.updateCommands();

        for (let i = 0; i < this.seats.length; ++i) {
            if (this.seats[i] === null || this.seats[i].user === null)
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
        $(`#seat-${i}`).finish().animate({opacity: 1});
        $(`#seat-${i}-tag`).off("click")
            .on("click", () => open(this.seats[i].user.profile.url))
            .attr("data-status", this.seats[i].status)
            .attr("data-original-title", this.seats[i].description);

        $(`#seat-${i}-avatar`).attr("src", this.seats[i].user.profile.gravatar_url);
        $(`#seat-${i}-username`).text(this.seats[i].user.username);
        $(`#seat-${i}-status`).text(this.seats[i].status === "Online" ? null : this.seats[i].status);

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
