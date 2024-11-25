document.addEventListener("DOMContentLoaded", function() {
    const conditionDescription = document.getElementById("conditionDescription");
    const conditions = ["Fever", "Cold", "Flu"];

    conditions.forEach(condition => {
        const button = document.createElement("button");
        button.textContent = condition;
        button.addEventListener("click", function() {
            conditionDescription.textContent = `Details about: ${condition}`;
        });
        conditionDescription.parentElement.appendChild(button);
    });
});
