document.addEventListener("DOMContentLoaded", function() {
    const removeSymptomButton = document.getElementById("removeSymptomButton");
    const symptomName = document.getElementById("symptomName");

    removeSymptomButton.addEventListener("click", function() {
        symptomName.textContent = "Symptom removed.";
    });
});
