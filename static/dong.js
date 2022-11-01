var score = 0
var lives = 4
var answerin = false

function lose() {
    console.log("lost score: "+score.toString())
    window.location.href= "/lost/"+score.toString()
}

function show_correct(q, correct) {
    $('#repeat-btn').toggleClass('hidden')
    $('#dong-btn').toggleClass('hidden')
    $('#nodong-btn').toggleClass('hidden')
    $('#repeat-btn').off()
    $('#play-btn').off()
    $('#dong-btn').off()
    $('#nodong-btn').off()
    $('#main_player').get(0).currentTime  = parseFloat(q['stop_time'])-1
    $('#main_player').get(0).play()
    if (correct) {
        // Set video to have a green filter 
        $('#video-filter').css('background-color', "green")
        $('#video-filter').toggleClass('hidden')
    } else {
        // Set video to have red filter
        $('#video-filter').css('background-color', "#BD3039")
        $('#video-filter').toggleClass('hidden')
    }
    setTimeout(function(){
        $('#main_player').get(0).pause()
        if (correct) {
            // Update Score
            score = score + 1
            $('#score').text("Score: " + score.toString()) 
        } else {
            // Decrement lives change outs and check for loss
            lives = lives-1
            $('#out_'+lives).addClass('red')
            if (lives == 1) {
                setTimeout(function(){
                    lose()
                }, 500)
            }
        }
        $('#video-filter').toggleClass('hidden')
        let q = qs.splice(Math.floor(Math.random()*qs.length), 1)[0]
        $('#loading-icon').removeClass('hidden')
        set_question(q)
    },9000);


}

function set_question(q) {
    $('#videoSrc').attr('src', q['url'])
    $('#main_player')[0].load()

    $('#main_player').on("loadeddata", function() {
        setTimeout(function(){
            $('#loading-icon').addClass('hidden')
            $("#play-btn").removeClass('hidden')
        }, 200)
       
    });

    $('#dong-btn').on( "click", function() {
        if (!answerin) {
            if (q['result'] == "homerun") {
                show_correct(q, true)
            } else {
                show_correct(q, false)
            }
        }
    });

    $('#nodong-btn').on( "click", function() {
        if (!answerin) {
            if (q['result'] != "homerun") {
                show_correct(q, true)
            } else {
                show_correct(q, false)
            }
        }
    });

    $('#play-btn').on( "click", function() {
        if (!answerin) {
            console.log("played")
            $("#play-btn").addClass('hidden')
            $('#main_player').get(0).currentTime  = 0
            $('#main_player').get(0).play()
            setTimeout(function(){
                $('#main_player').get(0).pause()
                $('#repeat-btn').toggleClass('hidden')
                $('#dong-btn').toggleClass('hidden')
                $('#nodong-btn').toggleClass('hidden')
            },parseFloat(q['stop_time'])*1000);
        }
    })

    $('#repeat-btn').on( "click", function() {
        if (!answerin) {
            console.log("repeat")
            $("#repeat-btn").toggleClass('hidden')
            start_time = 0//Math.max(0, parseFloat(q['stop_time'])-3)
            $('#main_player').get(0).currentTime  = start_time
            $('#main_player').get(0).play()
            setTimeout(function(){
                $('#main_player').get(0).pause()
                $('#repeat-btn').toggleClass('hidden')
            },parseFloat(q['stop_time'])*1000);
        }
    })
    
}

$(document).ready(function(){
    let q = qs.splice(Math.floor(Math.random()*qs.length), 1)[0]
    console.log(q)
    set_question(q)
})