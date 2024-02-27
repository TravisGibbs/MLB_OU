
function addText(text) {
    var textSpace = document.getElementById('textSpace')
    textSpace.textContent += text
}
$(document).ready(function(){
    if (message == "welcome") {
        $('#hide0').hide().delay(2000).fadeIn(1000);
        $('#hide1').hide().delay(4000).fadeIn(1000);
        $('#hide2').hide().delay(6000).fadeIn(1000);
        $('#hide3').hide().delay(10000).fadeIn(1000);
    }    
});

function setUpElevator() {
    var textSpace = document.getElementById('textSpace')
    textSpace.textContent =""

    var button0 = document.getElementById('button0');
    button0.style.cursor = 'pointer';
    button0.onclick = function() {
        addText("0")
    }
    button0.onmouseover = function() {
        button0.style.border = "6px solid red"
    }
    button0.onmouseleave = function() {
        button0.style.border = "4px solid red"
    }

    var button1 = document.getElementById('button1');
    button1.style.cursor = 'pointer';
    button1.onclick = function() {
        addText("1")
    }
    button1.onmouseover = function() {
        button1.style.border = "6px solid red"
    }
    button1.onmouseleave = function() {
        button1.style.border = "4px solid red"
    }

    var button2 = document.getElementById('button2');
    button2.style.cursor = 'pointer';
    button2.onclick = function() {
        addText("2")
    }
    button2.onmouseover = function() {
        button2.style.border = "6px solid red"
    }
    button2.onmouseleave = function() {
        button2.style.border = "4px solid red"
    }

    var button3 = document.getElementById('button3');
    button3.style.cursor = 'pointer';
    button3.onclick = function() {
        addText("3")
    }
    button3.onmouseover = function() {
        button3.style.border = "6px solid red"
    }
    button3.onmouseleave = function() {
        button3.style.border = "4px solid red"
    }

    var button4 = document.getElementById('button4');
    button4.style.cursor = 'pointer';
    button4.onclick = function() {
        addText("4")
    }
    button4.onmouseover = function() {
        button4.style.border = "6px solid red"
    }
    button4.onmouseleave = function() {
        button4.style.border = "4px solid red"
    }

    var button5 = document.getElementById('button5');
    button5.style.cursor = 'pointer';
    button5.onclick = function() {
        addText("5")
    }
    button5.onmouseover = function() {
        button5.style.border = "6px solid red"
    }
    button5.onmouseleave = function() {
        button5.style.border = "4px solid red"
    }

    var button6 = document.getElementById('button6');
    button6.style.cursor = 'pointer';
    button6.onclick = function() {
        addText("6")
    }
    button6.onmouseover = function() {
        button6.style.border = "6px solid red"
    }
    button6.onmouseleave = function() {
        button6.style.border = "4px solid red"
    }

    var button7 = document.getElementById('button7');
    button7.style.cursor = 'pointer';
    button7.onclick = function() {
        addText("7")
    }
    button7.onmouseover = function() {
        button7.style.border = "6px solid red"
    }
    button7.onmouseleave = function() {
        button7.style.border = "4px solid red"
    }

    var button8 = document.getElementById('button8');
    button8.style.cursor = 'pointer';
    button8.onclick = function() {
        addText("8")
    }
    button8.onmouseover = function() {
        button8.style.border = "6px solid red"
    }
    button8.onmouseleave = function() {
        button8.style.border = "4px solid red"
    }

    var button9 = document.getElementById('button9');
    button9.style.cursor = 'pointer';
    button9.onclick = function() {
        addText("9")
    }
    button9.onmouseover = function() {
        button9.style.border = "6px solid red"
    }
    button9.onmouseleave = function() {
        button9.style.border = "4px solid red"
    }

    var buttonA = document.getElementById('buttonA');
    buttonA.style.cursor = 'pointer';
    buttonA.onclick = function() {
        addText("A")
    }
    buttonA.onmouseover = function() {
        buttonA.style.border = "6px solid red"
    }
    buttonA.onmouseleave = function() {
        buttonA.style.border = "4px solid red"
    }

    var buttonB = document.getElementById('buttonB');
    buttonB.style.cursor = 'pointer';
    buttonB.onclick = function() {
        addText("B")
    }
    buttonB.onmouseover = function() {
        buttonB.style.border = "6px solid red"
    }
    buttonB.onmouseleave = function() {
        buttonB.style.border = "4px solid red"
    }

    var buttonC = document.getElementById('buttonC');
    buttonC.style.cursor = 'pointer';
    buttonC.onclick = function() {
        addText("C")
    }
    buttonC.onmouseover = function() {
        buttonC.style.border = "6px solid red"
    }
    buttonC.onmouseleave = function() {
        buttonC.style.border = "4px solid red"
    }

    var buttonD = document.getElementById('buttonD');
    buttonD.style.cursor = 'pointer';
    buttonD.onclick = function() {
        addText("D")
    }
    buttonD.onmouseover = function() {
        buttonD.style.border = "6px solid red"
    }
    buttonD.onmouseleave = function() {
        buttonD.style.border = "4px solid red"
    }

    var buttonE = document.getElementById('buttonE');
    buttonE.style.cursor = 'pointer';
    buttonE.onclick = function() {
        addText("E")
    }
    buttonE.onmouseover = function() {
        buttonE.style.border = "6px solid red"
    }
    buttonE.onmouseleave = function() {
        buttonE.style.border = "4px solid red"
    }

    var buttonF = document.getElementById('buttonF');
    buttonF.style.cursor = 'pointer';
    buttonF.onclick = function() {
        addText("F")
    }
    buttonF.onmouseover = function() {
        buttonF.style.border = "6px solid red"
    }
    buttonF.onmouseleave = function() {
        buttonF.style.border = "4px solid red"
    }

    var buttonClear = document.getElementById('buttonClear');
    buttonClear.style.cursor = 'pointer';
    buttonClear.onclick = function() {
        textSpace.textContent =""
    }
    buttonClear.onmouseover = function() {
        buttonClear.style.border = "6px solid red"
    }
    buttonClear.onmouseleave = function() {
        buttonClear.style.border = "4px solid red"
    }

    var buttonClose = document.getElementById('buttonClose');
    buttonClose.style.cursor = 'pointer';
    buttonClose.onclick = function() {
        if (textSpace.textContent.length == 0 || textSpace.textContent == null) {
            window.location.href='/image/empty'
        } else {
            window.location.href='/image/'+textSpace.textContent
        }
    }
    buttonClose.onmouseover = function() {
        buttonClose.style.border = "6px solid red"
    }
    buttonClose.onmouseleave = function() {
        buttonClose.style.border = "4px solid red"
    }

    var buttonOpen = document.getElementById('buttonOpen');
    buttonOpen.style.cursor = 'pointer';
    buttonOpen.onclick = function() {
        window.location.href='/'
    }
    buttonOpen.onmouseover = function() {
        buttonOpen.style.border = "6px solid red"
    }
    buttonOpen.onmouseleave = function() {
        buttonOpen.style.border = "4px solid red"
    }

    var buttonRandom = document.getElementById('buttonRandom');
    buttonRandom.style.cursor = 'pointer';
    buttonRandom.onclick = function() {
        window.location.href='/image/random'
    }
    buttonRandom.onmouseover = function() {
        buttonRandom.style.border = "6px solid red"
    }
    buttonRandom.onmouseleave = function() {
        buttonRandom.style.border = "4px solid red"
    }
}