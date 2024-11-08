document.addEventListener("DOMContentLoaded", function() {
    const diagnoseButton = document.getElementById("diagnoseButton");
    const selectBodyPart = document.getElementById("selectBodyPart");

    diagnoseButton.addEventListener("click", function() {
        alert(`Diagnosing symptoms for: ${selectBodyPart.value}`);
    });
});
