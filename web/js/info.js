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

function showSoilAdditionalInfo() {
    document.getElementById('additional-info').style.visibility = 'visible';
    document.getElementById('additional-info').children[0].children[0].innerHTML = "Soil Color";
    document.getElementById('additional-info-data-text-two').style.visibility = 'visible';
    document.getElementById('additional-info-data-text-one').innerHTML = document.getElementById('additional-info-indication-two').innerHTML;
    document.getElementById('additional-info-data-color').style.visibility = 'visible';
    document.getElementById('additional-info-indication-one').innerHTML = document.getElementById('additional-info-indication-four').innerHTML;
}

function showClimateAdditionalInfo() {
    document.getElementById('additional-info-data-text-two').style.visibility = 'hidden';
    document.getElementById('additional-info').style.visibility = 'visible';
    document.getElementById('additional-info').children[0].children[0].innerHTML = "Climate Data";
    document.getElementById('additional-info-data-text-one').innerHTML = document.getElementById('additional-info-indication-three').innerHTML + " inches of rainfall per month";
    document.getElementById('additional-info-data-color').style.visibility = 'hidden';
    if (parseInt(document.getElementById('additional-info-indication-three').innerHTML) < 4) {
        document.getElementById('additional-info-indication-one').innerHTML = 'Low Precipitation';
    } else {
        document.getElementById('additional-info-indication-one').innerHTML = 'High Precipitation';
    }
}

function removeAdditionalInfo() {
    document.getElementById('additional-info').style.visibility = 'hidden';
    document.getElementById('additional-info-data-color').style.visibility = 'hidden';
    document.getElementById('additional-info-data-text-two').style.visibility = 'hidden';
}

window.addEventListener('load', function() {
    console.log("hello");
    console.log(document.getElementById('additional-info-indication-two').innerHTML);
    if (document.getElementById('additional-info-indication-two').innerHTML.indexOf("organic") != -1) {
        var suggestionString = "Suggestion: ";
        suggestionString += "Less Fertilizer Required";
        if (parseInt(document.getElementById('additional-info-indication-three').innerHTML) < 4) {
            suggestionString += ", Adapt Irrigation for Greater Water Delivery";
        }
        document.getElementById('summary-subtitle').innerHTML = suggestionString;
    } else {
        var suggestionString = "Suggestion: ";
        suggestionString += "More Fertilizer Required";
        if (parseInt(document.getElementById('additional-info-indication-three').innerHTML) < 4) {
            suggestionString += ", Adapt Irrigation for Greater Water Delivery";
        }
        document.getElementById('summary-subtitle').innerHTML = suggestionString;
    }
    document.getElementById('summary-member-one-icon').addEventListener('mouseover', showSoilAdditionalInfo);
    document.getElementById('summary-member-two-icon').addEventListener('mouseover', showClimateAdditionalInfo);
    document.getElementById('summary-member-one-icon').addEventListener('mouseout', removeAdditionalInfo);
    document.getElementById('summary-member-two-icon').addEventListener('mouseout', removeAdditionalInfo);
})