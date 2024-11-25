let bodyMap = document.querySelector('.body-map');
let isFront = true;

function toggleImage() {
    if (isFront) {
        bodyMap.style.backgroundImage = "url('images/female_back.png')";
    } else {
        bodyMap.style.backgroundImage = "url('images/female_front.png')";
    }
    isFront = !isFront; // Toggle the state
}
