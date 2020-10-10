import {Room} from "./room.js";

class SequentialRoom extends Room {
    sounds = {
        info: new Audio("/static/gamemaster/sounds/info.wav"),
        alert: new Audio("/static/gamemaster/sounds/alert.wav"),
        success: new Audio("/static/gamemaster/sounds/success.wav"),
    };

    refresh() {
        super.refresh();

        if (this.seat !== null && this.seat.player !== null && this.seat.player.active)
            this.sounds.alert.play();
        else
            this.sounds.info.play();
    }

    updatePlayer(i) {
        super.updatePlayer(i);

        if (this.seats[i].player.active) {
            $(`#seat-${i}-progress-bar`).finish().animate({
                width: `${Math.floor(Math.max((1 - (Date.now() - room.updated_on) / room.timeout) * 100, 0))}%`,
            }, 0, "linear", function () {
                $(this).animate({
                    width: 0,
                }, Math.max(room.timeout - (Date.now() - room.updated_on), 0));
            });
        } else {
            $(`#seat-${i}-progress-bar`).finish().css("width", 0);
        }
    }
}

export {SequentialRoom};
