import {Room} from "./room.mjs";

class SequentialRoom extends Room {
    updatePlayer(i) {
        super.updatePlayer(i);

        if (this.seats[i].player.active) {
            $(`#seat-${i}-progress-bar`).finish().animate({
                width: `${Math.floor(Math.max((1 - (Date.now() - room.config.updated_on) / room.config.timeout) * 100, 0))}%`,
            }, 0, "linear", function () {
                $(this).animate({
                    width: 0,
                }, Math.max(room.config.timeout - (Date.now() - room.config.updated_on), 0));
            });
        } else {
            $(`#seat-${i}-progress-bar`).finish().css("width", 0);
        }
    }
}

export {SequentialRoom};
