var score = 0
var q_num = 0
var answer = 0
var left = 0
var right = 0
var answerin = false
var timeout = 1500
var lives = 4

function lose() {
    console.log("lost score: "+score.toString())
    window.location.href= "/lost/"+score.toString()
}

function wait(milliseconds){
    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });
  }

function set_players(players) {
    $('#player_col_1').css("background-image", "url("+players[0]["img"]+")")
    $('#player_col_2').css("background-image", "url("+players[1]["img"]+")")
    $('#player_text_1').text(players[0]['name'])
    $('#player_text_2').text(players[1]['name'])
}

function sleep (time) {
    return new Promise((resolve) => setTimeout(resolve, time));
  }

function set_question(q) {
    const  players = q['players']
    const col = q['col']

    $( '#player_col_2' ).removeClass('correct')
    $( '#player_col_1' ).removeClass('correct')

    set_players(players)
    console.log(players)
    if (players[0]['value'] > players[1]['value']) {
        answer = 0
    } else if (players[1]['value'] > players[0]['value']) {
        answer = 1
    } else {
        answer = 2
    }
    console.log(answer)
    let question_str = col
    $('#question').text(question_str)
}

$(document).ready(function(){
    var width = 0
    if (window.innerWidth/2 < 650) {
        width = innerWidth
        $('#form-con').removeClass('web-width')
        $('#form-con').addClass('mobile-width')
    } else {
        width =  window.innerWidth/2
    }

    set_question(qs[score])

    $('#front_1').hover(
        function() {
            if (!answerin) {
                $( '#front_1' ).addClass('selected')
            }
        }, function() {
            if (!answerin) {
                $( '#front_1' ).removeClass('selected')
            }
        }
      );

    $('#front_2').hover(
        function() {
            if (!answerin) {
                $( '#front_2' ).addClass('selected')
            }
        }, function() {
            if (!answerin) {
                $( '#front_2' ).removeClass('selected')
            }
        }
    );

    $('#front_1').click(function() {
        if (!answerin) {
            answerin = true
            // Animate numbers to show correct answer
            // Highlight correct player green and wait a few seconds
            $( '#front_1' ).removeClass('selected')
            $( '#front_2' ).removeClass('selected')
            $('#player_text_1').text(qs[q_num]['players'][0]['value'])
            $('#player_text_2').text(qs[q_num]['players'][1]['value'])
            if (answer == 0 || answer == 2) {
                $( '#front_1' ).addClass('correct')
                score = score + 1
            } else {
                $( '#front_1' ).addClass('wrong')
                lives = lives-1
                $('#out_'+lives).css("background-color", "#D50032")
                if (lives == 1) {
                    lose()
                }
            }
            $('#score').text("Score " + score.toString())
            q_num = q_num+1
            setTimeout(function(){
                $( '#front_1' ).removeClass('correct')
                $( '#front_1' ).removeClass('wrong')
                set_question(qs[q_num])     
                answerin = false
            },timeout);
        }
      });

    $('#front_2').click(function() {
        if (!answerin) {
            answerin = true
            // Animate numbers to show correct answer
            // Highlight correct player green and wait a few seconds
            $( '#front_1' ).removeClass('selected')
            $( '#front_2' ).removeClass('selected')
            $('#player_text_1').text(qs[q_num]['players'][0]['value'])
            $('#player_text_2').text(qs[q_num]['players'][1]['value'])
            if (answer == 1 || answer == 2) {
                $( '#front_2' ).addClass('correct')
                score = score+1
            } else {
                $( '#front_2' ).addClass('wrong')
                lives = lives-1
                $('#out_'+lives).css("background-color", "#D50032")
                if (lives == 1) {
                    lose()
                }
            }
            $('#score').text("Score " + score.toString())
            q_num = q_num+1
            setTimeout(function(){
                $( '#front_2' ).removeClass('correct')
                $( '#front_2' ).removeClass('wrong')
                set_question(qs[q_num])
                answerin = false     
            },timeout);
        }
    });
});