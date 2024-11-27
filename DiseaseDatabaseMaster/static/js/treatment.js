document.addEventListener("DOMContentLoaded", () => {
    console.log("Treatment page loaded successfully!");

    const treatments = document.querySelectorAll(".treatment-list li");

    treatments.forEach((treatment) => {
        treatment.addEventListener("click", () => {
            alert(`You selected: ${treatment.textContent}`);
        });
    });
});
