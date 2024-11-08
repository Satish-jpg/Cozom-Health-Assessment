document.addEventListener("DOMContentLoaded", function() {
    const bodyPartCombo = document.getElementById("bodyPartCombo");
    const symptomCombo = document.getElementById("symptomCombo");
    const addSymptomButton = document.getElementById("addSymptomButton");
    const conditionList = document.getElementById("conditionList");

    const bodyParts = ["Head", "Chest", "Leg", "Arm"];
    const symptoms = ["Pain", "Swelling", "Redness"];

    bodyParts.forEach(part => {
        const option = document.createElement("option");
        option.textContent = part;
        bodyPartCombo.appendChild(option);
    });

    symptoms.forEach(symptom => {
        const option = document.createElement("option");
        option.textContent = symptom;
        symptomCombo.appendChild(option);
    });

    addSymptomButton.addEventListener("click", function() {
        const selectedBodyPart = bodyPartCombo.value;
        const selectedSymptom = symptomCombo.value;
        const listItem = document.createElement("li");
        listItem.textContent = `Symptom: ${selectedSymptom} in ${selectedBodyPart}`;
        conditionList.appendChild(listItem);
    });
});
