// document.addEventListener("DOMContentLoaded", function () {
//     document.getElementById('playSpeech').addEventListener('click', function () {
//         let text = document.getElementById('textInput').value;
//         let voice = document.getElementById('voiceSelect').value;
//         let rate = document.getElementById('rateInput').value;
//         let volume = document.getElementById('volumeInput').value;

//         if (text.trim() === "") {
//             alert("Please enter some text!");
//             return;
//         }

//         // Send AJAX request to Django API
//         fetch(`/api/tts/?text=${encodeURIComponent(text)}&voice_type=${voice}&rate=${rate}&volume=${volume}`)
//         .then(response => response.json())
//         .then(data => {
//             console.log(data.message);
//         })
//         .catch(error => console.error('Error:', error));
//     });
// });


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('playSpeech').addEventListener('click', function () {
        let text = document.getElementById('textInput').value;

        if (text.trim() === "") {
            alert("Please enter some text!");
            return;
        }

        // Fetch the MP3 file from the API
        fetch(`/api/tts/?text=${encodeURIComponent(text)}`)
        .then(response => response.blob())
        .then(blob => {
            let audioUrl = URL.createObjectURL(blob);
            let audio = new Audio(audioUrl);
            audio.play();
        })
        .catch(error => console.error('Error:', error));
    });
});
