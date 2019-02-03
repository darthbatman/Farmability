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

function showAdditionalInfo() {
    document.getElementById('additional-info').style.visibility = 'visible';
}

function removeAdditionalInfo() {
    document.getElementById('additional-info').style.visibility = 'hidden';
}

window.addEventListener('load', function() {
    document.getElementById('summary-member-one-icon').addEventListener('mouseover', showAdditionalInfo);
    document.getElementById('summary-member-two-icon').addEventListener('mouseover', showAdditionalInfo);
    document.getElementById('summary-member-one-icon').addEventListener('mouseout', removeAdditionalInfo);
    document.getElementById('summary-member-two-icon').addEventListener('mouseout', removeAdditionalInfo);
})