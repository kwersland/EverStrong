exercises = "https://wger.de/api/v2/exercise"
muscles = "https://wger.de/api/v2/muscle" 

function play(elem) {
    elem.play()
}

function pause(elem) {
    elem.pause();
    elem.currentTime = 0.0;
}

function on(id) {
        document.getElementById(id).style.display = "block";
}
function off(id) {
    document.getElementById(id).style.display = "none";
}

function change() {
    document.getElementById("dropdown_image").src="static/img/96_flipped.png"
}

function revert() {
    document.getElementById("dropdown_image").src="static/img/96.png"
}

function getMuscles() {
    selectMuscle = document.querySelector("#muscle")
    fetch(muscles)
        .then(response => response.json())
        .then(data => {
            for (i = 0; i < 15; i++) {
                console.log(data.results[i])
                if (!data.results[i]['name_en']){
                    continue
                }
                else {
                    selectMuscle.innerHTML += `
                    <option>${data.results[i]['name_en']}</option>
                    `
                }
            }
        })
}