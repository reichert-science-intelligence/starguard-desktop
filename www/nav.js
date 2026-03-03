// StarGuard AI Navigation — Event Delegation
// Catches clicks on .sg-nav-link elements and sends to Shiny
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(e) {
        var el = e.target.closest('.sg-nav-link');
        if (el && el.dataset.nav) {
            console.log('NAV CLICK:', el.dataset.nav);
            // Remove active class from all nav links
            document.querySelectorAll('.sg-nav-link').forEach(function(link) {
                link.classList.remove('sg-nav-active');
            });
            // Add active class to clicked link
            el.classList.add('sg-nav-active');
            // Send to Shiny
            if (window.Shiny && Shiny.setInputValue) {
                Shiny.setInputValue('nav_target', el.dataset.nav, {priority: 'event'});
            } else {
                // Shiny not ready yet, retry after short delay
                setTimeout(function() {
                    Shiny.setInputValue('nav_target', el.dataset.nav, {priority: 'event'});
                }, 500);
            }
        }
    });

    // Set Home as active on load
    var homeLink = document.querySelector('.sg-nav-link[data-nav="home"]');
    if (homeLink) homeLink.classList.add('sg-nav-active');

    console.log('StarGuard nav.js loaded — event delegation active');
});
