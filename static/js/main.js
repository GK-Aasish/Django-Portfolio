/**
 * TYPEWRITER ENGINE
 * Designed to handle multi-line strings with \n
 */

const typewriterElement = document.getElementById('typewriter');

// THE PHRASES: Use \n where you want the line to break
const phrases = [
    "A Full-Stack Web\nDeveloper", 
    "3D Artist",
    "Creative Problem\nSolver"
];

let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;
let typeSpeed = 150;

function typeWithCursor() {
    const currentPhrase = phrases[phraseIndex];

    if (isDeleting) {
        // Erasing logic
        charIndex--;
        typeSpeed = 50; // Erase faster than you type
    } else {
        // Typing logic
        charIndex++;
        typeSpeed = 150; // Standard typing speed
    }

    // Extract the current slice of text
    const textToShow = currentPhrase.substring(0, charIndex);
    
    // Inject the text AND the cursor span
    // We use innerHTML so that the <span class="cursor"> remains part of the line
    typewriterElement.innerHTML = textToShow + '<span class="cursor"></span>';

    // --- STATE SWITCHING LOGIC ---

    // 1. If we finished typing the whole phrase
    if (!isDeleting && charIndex === currentPhrase.length) {
        isDeleting = true;
        typeSpeed = 2000; // Pause at the end of a sentence so people can read it
    } 
    // 2. If we finished deleting the whole phrase
    else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        phraseIndex = (phraseIndex + 1) % phrases.length; // Cycle back to first phrase
        typeSpeed = 500; // Pause briefly before starting the next phrase
    }

    // Run the function again after the delay
    setTimeout(typeWithCursor, typeSpeed);
}

// Start the animation once the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    typeWithCursor();
});