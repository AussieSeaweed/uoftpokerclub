import {SequentialRoom} from "./sequential.mjs";

class TicTacToeRoom extends SequentialRoom {
    constructor() {
        super();

        for (let r = 0; r < 3; ++r)
            for (let c = 0; c < 3; ++c)
                $(`#board-${r}-${c}`).click(() => this.send(`Mark ${r} ${c}`));
    }

    updateContext() {
        super.updateContext();

        for (let r = 0; r < 3; ++r)
            for (let c = 0; c < 3; ++c)
                $(`#board-${r}-${c}`).attr("data-index", this.context.board[r][c]);

        if (this.context.winning_coords !== null)
            for (let [r, c] of this.context.winning_coords)
                $(`#board-${r}-${c}`).attr("data-index", "2");
    }

    clearContext() {
        super.updateContext();

        for (let r = 0; r < 3; ++r)
            for (let c = 0; c < 3; ++c)
                $(`#board-${r}-${c}`).attr("data-index", null);
    }
}

export {TicTacToeRoom};
