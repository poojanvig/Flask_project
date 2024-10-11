// Toggle Side Menu
function toggleMenu() {
    const menu = document.getElementById("sideMenu");
    if (menu.classList.contains("active")) {
        menu.classList.remove("active");
    } else {
        menu.classList.add("active");
    }
}

// Shrink Navbar on Scroll
window.onscroll = function() {
    const navbar = document.getElementById("navbar");
    const logoText = document.getElementById("mainName");
    if (document.documentElement.scrollTop > 50) {
        navbar.classList.add("small");
        logoText.style.display = "none"; // Hide logo text when scrolling down
    } else {
        navbar.classList.remove("small");
        logoText.style.display = "block"; // Show logo text when at top
    }
};
