$(document).ready(function() {
    // The 'images' array from home.html is used here.
    if (typeof images === 'undefined') { return; }

    const container = $('.image-window-container');
    // We create the filmstrip dynamically for robustness
    container.wrapInner('<div class="filmstrip"></div>');
    const filmstrip = container.find('.filmstrip');
    const windows = filmstrip.find('.image-window');

    // --- Step 1: Initial Setup ---
    function initializeCarousel() {
        // Set the initial image sources
        $(windows[0]).find('img').attr('src', images[2]); // Left gets Img 3
        $(windows[1]).find('img').attr('src', images[0]); // Center gets Img 1
        $(windows[2]).find('img').attr('src', images[1]); // Right gets Img 2

        // Set the initial styling classes
        updateClasses();
    }

    // --- Step 2: Function to apply styling based on position ---
    function updateClasses() {
        const currentWindows = filmstrip.find('.image-window');
        currentWindows.removeClass('center-window side-window');

        // The window at index 1 is ALWAYS the center.
        currentWindows.eq(1).addClass('center-window');
        // The windows at index 0 and 2 are ALWAYS the sides.
        currentWindows.eq(0).addClass('side-window');
        currentWindows.eq(2).addClass('side-window');
    }

    // --- Step 3: The slide animation ---
    function slide() {
        const windowWidth = windows.first().outerWidth(true);

        // Animate the filmstrip to the left
        filmstrip.animate(
            { left: -windowWidth },
            800, // Animation speed
            'swing',
            function() { // After animation is complete...
                // Move the first window to the end of the line
                filmstrip.append(filmstrip.find('.image-window').first());
                // Instantly reset the filmstrip's position
                filmstrip.css({ left: '0px' });
                // Re-apply the styling classes to the new order of windows
                updateClasses();
            }
        );
    }

    // --- Run Everything ---
    initializeCarousel();
    setInterval(slide, 3000); // Rotate every 3 seconds
});