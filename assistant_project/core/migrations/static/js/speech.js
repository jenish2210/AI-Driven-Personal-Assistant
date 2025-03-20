document.getElementById("startRecording").addEventListener("click", function () {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.onresult = function (event) {
        let transcript = event.results[0][0].transcript;
        document.getElementById("textInput").value = transcript; // Show text in input box
    };

    recognition.onerror = function (event) {
        console.error("Speech recognition error:", event.error);
    };

    recognition.start();
});



document.getElementById("startRecording").addEventListener("click", function () {
    fetch("/api/speech-to-text/")
        .then(response => response.json())
        .then(data => {
            document.getElementById("textInput").value = data.text || "Error in recognition";
        })
        .catch(error => console.error("Error:", error));
});
