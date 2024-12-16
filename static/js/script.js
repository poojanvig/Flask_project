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

      let currentIndex = 0;
        const projects = document.getElementById('projects');
        const totalProjects = projects.children.length;
        const maxVisibleProjects = 3;

        function updateSlidePosition() {
            const projectWidth = projects.children[0].clientWidth + 20; // 20px for margin
            projects.style.transform = `translateX(-${currentIndex * projectWidth}px)`;
        }

        function nextSlide() {
            if (currentIndex < totalProjects - maxVisibleProjects) {
                currentIndex++;
                updateSlidePosition();
            }
        }

        function prevSlide() {
            if (currentIndex > 0) {
                currentIndex--;
                updateSlidePosition();
            }
        }

        window.addEventListener('resize', () => {
            updateSlidePosition();
        });
// Blogs

let blogCurrentIndex = 0;

function moveBlogSlide(direction) {
    const carousel = document.querySelector('.carousel-blogs');
    const blogs = document.querySelectorAll('.carousel-blogs .blog-post');
    const totalBlogs = blogs.length;
    const blogsPerView = 3; // Always display 3 items per view

    // Calculate maximum possible index
    const maxIndex = Math.ceil(totalBlogs / blogsPerView) - 1;

    // Update the current index based on direction
    blogCurrentIndex += direction;

    // Keep the index within bounds
    if (blogCurrentIndex < 0) {
        blogCurrentIndex = maxIndex;
    } else if (blogCurrentIndex > maxIndex) {
        blogCurrentIndex = 0;
    }

    // Calculate the offset for the carousel
    const offset = -blogCurrentIndex * 100;

    // Apply the transform to slide the blogs
    carousel.style.transform = `translateX(${offset}%)`;
}
