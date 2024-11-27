// Ensure the DOM is fully loaded before executing
document.addEventListener('DOMContentLoaded', () => {
    const homeButton = document.querySelector('.home-button');

    if (homeButton) {
        homeButton.addEventListener('click', () => {
            alert('Redirecting you to the Home Page!');
        });
    }
});
