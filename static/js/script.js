// JavaScript to toggle the side menu and make the navbar shrink on scroll
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    const logoText = document.getElementById('logoText');
    if (window.scrollY > 50) {
        navbar.classList.add('shrink');
        logoText.classList.add('hidden');
    } else {
        navbar.classList.remove('shrink');
        logoText.classList.remove('hidden');
    }
});

// JavaScript for toggling the side menu
const menuIcon = document.querySelector('.menu-icon');
const sideMenu = document.getElementById('sideMenu');
const closeMenu = document.querySelector('.close-menu');
const bookVisitButton = document.getElementById('bookVisitButton');
const menuBookVisit = document.getElementById('menuBookVisit');

menuIcon.addEventListener('click', () => {
    sideMenu.classList.add('active');
});

closeMenu.addEventListener('click', () => {
    sideMenu.classList.remove('active');
});

// Adjust the Book Visit button visibility on different screen sizes
function adjustBookVisit() {
    if (window.innerWidth <= 768) {
        bookVisitButton.style.display = 'none';
        menuBookVisit.style.display = 'block';
    } else {
        bookVisitButton.style.display = 'block';
        menuBookVisit.style.display = 'none';
    }
}

// Run function on load and resize
window.addEventListener('load', adjustBookVisit);
window.addEventListener('resize', adjustBookVisit);

// Functionality for "Book a Site Visit" when clicked from side menu
function bookSiteVisit() {
    alert('Redirecting to book a site visit...');
}
