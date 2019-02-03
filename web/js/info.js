function getRGB() {
    var canvas = document.getElementById("canvas")
    var pixelData = canvas.getContext('2d').getImageData(event.offsetX, event.offsetY, 1, 1).data;
    $.ajax({
        type: "POST",
        url: canvas.src,
        data: JSON.stringify({ 
            R: pixelData[0],
            G: pixelData[1],
            B: pixelData[2]
        } ),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
    });
}