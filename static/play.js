var score = 0
var answer = 0
var left = 0
var right = 0


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
    const row = q['row']

    $( '#player_col_2' ).removeClass('correct')
    $( '#player_col_1' ).removeClass('correct')

    set_players(players)

    if (players[0]['value'] > players[1]['value']) {
        answer = 0
    } else if (players[1]['value'] > players[0]['value']) {
        answer = 1
    } else {
        answer = 2
    }
    let question_str = "Who had more " + col
    if (row == "totals") {
        question_str += " in their career?"
    } else {
        question_str += " on avg per 162 game season?"
    }
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

    $('#player_col_1').hover(
        function() {
            
          $( '#player_col_1' ).addClass('selected')
        }, function() {
          $( '#player_col_1' ).removeClass('selected')
        }
      );

    $('#player_col_2').hover(
        function() {
            $( '#player_col_2' ).addClass('selected')
        }, function() {
            $( '#player_col_2' ).removeClass('selected')
        }
    );

    $('#player_col_1').click(function() {
        // Animate numbers to show correct answer
        // Highlight correct player green and wait a few seconds
        $( '#player_col_1' ).removeClass('selected')
        $( '#player_col_2' ).removeClass('selected')
        if (answer == 0 || answer == 2) {
            $( '#player_col_1' ).addClass('correct')
            console.log("here")
        }
        score = score+1
        setTimeout(function(){
            set_question(qs[score])     
        },5000);

      });

    $('#player_col_2').click(function() {
        // Animate numbers to show correct answer
        // Highlight correct player green and wait a few seconds
        $( '#player_col_1' ).removeClass('selected')
        $( '#player_col_2' ).removeClass('selected')
        if (answer == 1 || answer == 2) {
            $( '#player_col_2' ).addClass('correct')
            console.log("here")
        }
        score = score+1
        setTimeout(function(){
            set_question(qs[score])     
        },5000);
           
    });
});