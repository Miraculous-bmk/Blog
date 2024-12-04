// blog.js (or a new JS file linked to your base.html)
document.addEventListener('DOMContentLoaded', function() {
    const modeToggle = document.getElementById('mode-icon');
    const body = document.body;

    // Check local storage for theme preference
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-theme');
        modeToggle.classList.remove('fa-sun');
        modeToggle.classList.add('fa-moon');
    } else {
        body.classList.remove('dark-theme');
        modeToggle.classList.remove('fa-moon');
        modeToggle.classList.add('fa-sun');
    }

    // Toggle dark/light mode
    modeToggle.addEventListener('click', function() {
        body.classList.toggle('dark-theme');
        
        if (body.classList.contains('dark-theme')) {
            modeToggle.classList.remove('fa-sun');
            modeToggle.classList.add('fa-moon');
            localStorage.setItem('theme', 'dark');
        } else {
            modeToggle.classList.remove('fa-moon');
            modeToggle.classList.add('fa-sun');
            localStorage.setItem('theme', 'light');
        }
    });
});
