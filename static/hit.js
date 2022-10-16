function new_q() {
    console.log("played!")
    $("#main_player").get(0).play()
    console.log(end_time)
    setTimeout(function(){
        $("#main_player").get(0).pause();
    },parseFloat(end_time)*1000);
}

$(document).ready(function(){
    var socket = io()
    document.getElementById("main_player").addEventListener('timeupdate', function() {
        currentTime = this.currentTime;
    });
    $("#play-btn").click(function() {
        setTimeout(function(){
            new_q()
        },100);
    })

    $('#set-btn').click(function(){
        socket.emit('update',
        {'key':label, 'value':document.getElementById("main_player").currentTime})
        window.location.reload();
    });

})