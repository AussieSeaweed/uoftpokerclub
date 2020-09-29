import {Room} from "./room.mjs";

class SequentialRoom extends Room {
    updatePlayer(i) {
        super.updatePlayer(i);

        $(`#seat-${i}-progress-bar`).css("width", this.seats[i].player.active ? "100%" : "0%");
    }
}

export {SequentialRoom};
