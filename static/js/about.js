document.addEventListener("DOMContentLoaded", function() {
    const agreeButton = document.getElementById("agreeButton");
    const disagreeButton = document.getElementById("disagreeButton");

    agreeButton.addEventListener("click", function() {
        alert("Thank you for agreeing!");
    });

    disagreeButton.addEventListener("click", function() {
        alert("Please let us know how we can improve.");
    });
});
