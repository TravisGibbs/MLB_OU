const colorMap = new Map();
colorMap.set("0", "color0");
colorMap.set("1", "color1");
colorMap.set("2", "color2");
colorMap.set("3", "color3");
colorMap.set("4", "color4");
colorMap.set("5", "color5");
colorMap.set("6", "color6");
colorMap.set("7", "color7");
colorMap.set("8", "color8");
colorMap.set("9", "color9");
colorMap.set("A", "color10");
colorMap.set("B", "color11");
colorMap.set("C", "color12");
colorMap.set("D", "color13");
colorMap.set("E", "color14");
colorMap.set("F", "color15");

const bwColorMap = new Map()
bwColorMap.set("0", "color16");
bwColorMap.set("1", "color17");
bwColorMap.set("2", "color18");
bwColorMap.set("3", "color19");
bwColorMap.set("4", "color20");
bwColorMap.set("5", "color21");
bwColorMap.set("6", "color22");
bwColorMap.set("7", "color23");
bwColorMap.set("8", "color24");
bwColorMap.set("9", "color25");
bwColorMap.set("A", "color26");
bwColorMap.set("B", "color27");
bwColorMap.set("C", "color28");
bwColorMap.set("D", "color29");
bwColorMap.set("E", "color30");
bwColorMap.set("F", "color31");

function chunk(arr, size, out) {

    // if the output array hasn't been passed in
    // create it
    out = out || [];
  
    // if there are no elements in the input array
    // return the output array
    if (!arr.length) return out;
  
    // push the "head" of the input array to the
    // output array
    out.push(arr.slice(0, size));
  
    // call chunk again with the "tail" of the input array
    return chunk(arr.slice(size), size, out);
  }

function convert(arr) {
    new_arr = []
    arr.forEach(element => {
        new_arr.push(colorMap.get(element))
    });
    return new_arr
}

function generate_picture(colorString) {
    color_arr = colorString.split("")

    return chunk(convert(color_arr), 64)
}

$(document).ready(function(){
    const pictureArray = generate_picture(image)

    mainContainer =  document.getElementById("main")
    for (i = 0; i < 64; i++) {
        let rowValues = pictureArray[i]
        let newRow = document.createElement("div")
        newRow.className ="row"
        rowValues.forEach(pixel => {
            let newPixel = document.createElement("span")
            newPixel.className = "pixel " + pixel
            newRow.appendChild(newPixel)
        });
        mainContainer.appendChild(newRow)
    }

    let trace = document.getElementById("trace")
    trace.textContent = input
});