import {SequentialRoom} from "./sequential.js";

class PokerRoom extends SequentialRoom {
    constructor() {
        super();

        $("#action-put-range").change(function () {
            let minAmount = parseInt($(this).attr("data-min-amount")),
                maxAmount = parseInt($(this).attr("data-max-amount"));

            let value = Math.max(minAmount, Math.min(maxAmount, Math.round(minAmount + (maxAmount - minAmount) *
                Math.pow($(this).val() / 100, 2)
            )));

            $("#action-put-amount").text(value);
        }).on("input", function () {
            $(this).change();
        });

        $("#action-put").click(() => this.send(`${$("#action-put-label").text()} ${$("#action-put-amount").text()}`));
        $("#action-continue").click(() => this.send($("#action-continue-label").text()));
        $("#action-surrender").click(() => this.send($("#action-surrender-label").text()));
    }

    updatePlayer(i) {
        super.updatePlayer(i);

        $(`#seat-${i}-stack`).text(this.seats[i].player.stack);

        $(`#seat-${i}-bet`).text(this.seats[i].player.bet === 0 ? null : this.seats[i].player.bet);
        $(`#seat-${i}-button`).finish().animate({
            opacity: this.seats[i].player.index === Math.max(...this.players.map(player => player.index))
        });

        for (let j = 0; j < (this.seats[i].player.cards === null ? 0 : this.seats[i].player.cards.length); ++j)
            $(`#seat-${i}-card-${j}`).attr("src", this.cardImagePath(this.seats[i].player.cards[j]))
                .finish()
                .animate({opacity: 1});

        for (let j = this.seats[i].player.cards === null ? 0 : this.seats[i].player.cards.length; j < this.config.num_hole_cards; ++j)
            $(`#seat-${i}-card-${j}`).attr("src", this.cardImagePath(null))
                .finish()
                .animate({opacity: 0});
    }

    clearPlayer(i) {
        super.clearPlayer(i);

        $(`#seat-${i}-stack`).text(null);

        $(`#seat-${i}-bet`).text(null);
        $(`#seat-${i}-button`).finish().animate({opacity: 0});

        for (let j = 0; j < this.config.num_hole_cards; ++j)
            $(`#seat-${i}-card-${j}`).attr("src", this.cardImagePath(null))
                .finish()
                .animate({opacity: 0});
    }

    updateContext() {
        super.updateContext();

        $("#pot").text(this.context.pot);

        for (let i = 0; i < this.context.board.length; ++i)
            $(`#board-card-${i}`).attr("src", this.cardImagePath(this.context.board[i]))
                .finish()
                .animate({opacity: 1});

        for (let i = this.context.board.length; i < this.config.num_board_cards; ++i)
            $(`#board-card-${i}`).attr("src", this.cardImagePath(null))
                .finish()
                .animate({opacity: 0});
    }

    clearContext() {
        super.clearContext();

        $("#pot").text(null);

        for (let i = 0; i < this.config.num_board_cards; ++i)
            $(`#board-card-${i}`).attr("src", this.cardImagePath(null))
                .finish()
                .animate({opacity: 0});
    }

    updateActions() {
        super.updateActions();

        $("#action").fadeIn();

        let putLabel, minPutAmount, maxPutAmount, continueLabel, surrenderLabel;

        for (let action of this.actions) {
            if (action.startsWith("Bet") || action.startsWith("Raise")) {
                let tokens = action.split(" "), amount = parseInt(tokens[1]);
                putLabel = tokens[0];
                minPutAmount = minPutAmount ? Math.min(minPutAmount, amount) : amount;
                maxPutAmount = maxPutAmount ? Math.max(maxPutAmount, amount) : amount;
            } else if (action.startsWith("Call") || action.startsWith("Check"))
                continueLabel = action;
            else
                surrenderLabel = action;
        }


        if (putLabel) {
            $("#action-put").show();
            $("#action-put-label").text(putLabel);

            if (minPutAmount !== maxPutAmount)
                $("#action-put-range").show().val(0)
                    .attr("data-min-amount", minPutAmount)
                    .attr("data-max-amount", maxPutAmount)
                    .change();
            else
                $("#action-put-range").hide().val(0)
                    .attr("data-min-amount", minPutAmount)
                    .attr("data-max-amount", maxPutAmount)
                    .change();
        } else {
            $("#action-put").hide();
            $("#action-put-range").hide();
        }

        if (continueLabel) {
            $("#action-continue-label").text(continueLabel);
        }

        if (surrenderLabel) {
            $("#action-surrender").show();
            $("#action-surrender-label").text(surrenderLabel);
        } else {
            $("#action-surrender").hide();
        }
    }

    clearActions() {
        super.clearActions();

        $("#action").fadeOut();
    }

    cardImagePath(card) {
        return `/static/gamemaster/images/cards/${card}.png`;
    }
}

export {PokerRoom};
