var alanBtnInstance = alanBtn({

    key: "385a1f3a0f8a7e878d63f1d3eb47545d2e956eca572e1d8b807a3e2338fdd0dc/stage",
    onCommand: function (commandData) {
        if (commandData.command === "submit") {
            //call client code that will react on the received command
            submit();
        }
        if (commandData.command === "play_video") {
            play_video();
        }
        if (commandData.command === "stop_video") {
            stop_video();
        }
    },
    rootEl: document.getElementById("alan-btn"),
});

function submit() {
    document.getElementById("analyzeCommentsButton").click();
    console.log("Submitted");
}

function play_video() {
    jQuery(function ($) {
        let ytURL = $("#videoPlayer")[0].src.split('?')[0]
        console.log(ytURL)
        $("#videoPlayer")[0].src = ytURL + "?rel=0&autoplay=1";
        console.log("Playing", $("#videoPlayer")[0].src)
    });
}

function stop_video() {
    jQuery(function ($) {
        let ytURL = $("#videoPlayer")[0].src.split('?')[0]
        console.log(ytURL)
        $("#videoPlayer")[0].src = ytURL;
        console.log("Stopping", $("#videoPlayer")[0].src)
    });
}

function validateForm() {
    document.getElementById("errorMessage").style.display = "none";
    var ytURL = document.forms["youtubeURLForm"].elements[0].value
    pattern = /https:\/\/www.youtube.com\/watch\?v=.{11}/

    if (ytURL == "") {
        document.getElementById("errorMessage").innerHTML = "Enter a Youtube video URL to see the comment analysis"
        document.getElementById("errorMessage").style.display = "block";
        alanBtnInstance.playText('The URL field is empty');
        return false;
    }

    else if (pattern.test(ytURL) == false) {
        document.getElementById("errorMessage").innerHTML = "Please enter a valid URL in the form https://www.youtube.com/watch?v=videoID"
        document.getElementById("errorMessage").style.display = "block";
        alanBtnInstance.playText('Please enter Valid Youtube URL')
        return false;
    }
    else {
        document.getElementById("errorMessage").style.display = "none";
        return true;
    }
}
