// main.js
document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle (add a button with class "nav-toggle" in your HTML)
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
  
    if (navToggle) {
      navToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
      });
    }
  });
  