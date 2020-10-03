function getWebsocketProtocol() {
    return location.protocol === "https:" ? "wss:" : "ws:";
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});
