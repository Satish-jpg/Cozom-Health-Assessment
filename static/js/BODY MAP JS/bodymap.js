document.addEventListener("DOMContentLoaded", function () {
    const bodyMap = document.querySelector('map[name="maleBodyMap"]');
    const selectedPartDisplay = document.getElementById("selectedPart");

    bodyMap.addEventListener("click", function (event) {
        const area = event.target;
        if (area.tagName.toLowerCase() === 'area') {
            const bodyPart = area.getAttribute("data-part");
            selectedPartDisplay.textContent = `You selected: ${bodyPart}`;
            // JSON data from body_parts.json could be used here to show additional details
        }
    });
});
