var score = 0
var q_num = 0
var answer = 0
var left = 0
var right = 0
var answerin = false
var timeout = 2000
var lives = 4

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      obj.innerHTML = Math.floor(progress * (end - start) + start);
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };
    window.requestAnimationFrame(step);
  }

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
    // const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
    // const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
    // var height = window.innerHeight
    // var width = window.innerWidth
    // if (window.innerWidth/2 < 650) {
    //     $('#outs').css('margin-top', (height*4/5).toString()+"px !important")
    // }

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

            let text_1 = document.getElementById('player_text_1');
            let text_2 = document.getElementById('player_text_2');
            animateValue(text_1, 0, qs[q_num]['players'][0]['value'], 500)
            animateValue(text_2, 0, qs[q_num]['players'][1]['value'], 500)

            
            setTimeout(function() {
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
            }, 550)
            
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
            let text_1 = document.getElementById('player_text_1');
            let text_2 = document.getElementById('player_text_2');
            animateValue(text_1, 0, qs[q_num]['players'][0]['value'], 500)
            animateValue(text_2, 0, qs[q_num]['players'][1]['value'], 500)

            setTimeout(function() {
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
            }, 550)
            
            $('#score').text("Score: " + score.toString())
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