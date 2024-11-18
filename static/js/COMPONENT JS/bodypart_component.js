document.addEventListener("DOMContentLoaded", function() {
    const bodyPartSelection = document.getElementById("bodyPartSelection");
    const bodyParts = ["Head", "Chest", "Arm", "Leg"];

    bodyParts.forEach(part => {
        const button = document.createElement("button");
        button.textContent = part;
        button.addEventListener("click", function() {
            alert(`Body Part Selected: ${part}`);
        });
        bodyPartSelection.appendChild(button);
    });
});
