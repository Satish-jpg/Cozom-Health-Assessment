document.addEventListener('DOMContentLoaded', () => {
    const agreeButton = document.getElementById('agreeButton');
    const disagreeButton = document.getElementById('disagreeButton');

    agreeButton.addEventListener('click', () => {
        alert('Thank you for agreeing to our terms!');
    });

    disagreeButton.addEventListener('click', () => {
        alert('You disagreed. Feel free to explore our platform further!');
    });
});
