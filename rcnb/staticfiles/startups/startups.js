// startups/static/startups/startups.js

document.addEventListener('DOMContentLoaded', () => {
    // Handle the "More Info" image popup
    const moreInfoButtons = document.querySelectorAll('.more-btn');
    const popupOverlay = document.getElementById('imagePopup');
    const popupImage = document.getElementById('popupImage');
    const closeButton = document.querySelector('.close-button');

    moreInfoButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const imageUrl = event.target.dataset.image;
            if (imageUrl) {
                popupImage.src = imageUrl;
                popupOverlay.style.display = 'flex';
            }
        });
    });

    closeButton.addEventListener('click', () => {
        popupOverlay.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === popupOverlay) {
            popupOverlay.style.display = 'none';
        }
    });
});