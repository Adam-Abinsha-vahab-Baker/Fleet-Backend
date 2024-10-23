
const instructionsButton = document.getElementById('instructionsButton');
const instructionsModal = document.getElementById('instructionsModal');
const overlay = document.getElementById('overlay');


instructionsButton.addEventListener('click', () => {
    instructionsModal.style.display = 'block';
    overlay.style.display = 'block';
});


function closeInstructionsModal() {
    instructionsModal.style.display = 'none';
    overlay.style.display = 'none';
}

function closeAllModals() {
    // Close other modals if they are open
    closeTripModal();
    closeAddCustomerDialog(); 
    closeInstructionsModal();
}


overlay.addEventListener('click', closeAllModals);
