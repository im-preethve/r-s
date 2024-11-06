// Form submission handling
document.getElementById('orderForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get form data
    const customerName = document.getElementById('customerName').value;
    const customerNumber = document.getElementById('customerNumber').value;
    const foodName = document.getElementById('foodName').value;
    const additionalFood = document.getElementById('additionalFood').value;
    const orderQuantity = document.getElementById('orderQuantity').value;
    const orderTime = document.getElementById('orderTime').value;

    // Create an object to send
    const orderData = {
        name: customerName,
        number: customerNumber,
        order: foodName,
        additional: additionalFood,
        quantity: orderQuantity,
        order_time: orderTime
    };

    // Send data to the backend
    fetch('/api/order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Optionally, reset the form or show a success message
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// Navbar toggle functionality
let menu = document.querySelector('#menu-bars');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
}

// Section scroll functionality
let section = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header .navbar a');

window.onscroll = () => {
    menu.classList.remove('fa-times'); 
    navbar.classList.remove('active'); 

    section.forEach(sec => {
        let top = window.scrollY;
        let height = sec.offsetHeight;
        let offset = sec.offsetTop - 150;
        let id = sec.getAttribute('id');

        if(top >= offset && top < offset + height) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                document.querySelector('header .navbar a[href*=' + id + ']').classList.add('active');
            });
        }
    });
};

// Search form toggle functionality
document.querySelector('#search-icon').onclick = () => {
    document.querySelector('#search-form').classList.toggle('active');
}

document.querySelector('#close').onclick = () => {
    document.querySelector('#search-form').classList.remove('active');
}

// Swiper sliders initialization
var homeSwiper = new Swiper(".home-slider", {
    spaceBetween: 30,
    centeredSlides: true,
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    loop: true,
});

var reviewSwiper = new Swiper(".review-slider", {
    spaceBetween: 30,
    centeredSlides: true,
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
    loop: true,
    slidesPerView: 1,
    breakpoints: {
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
    },
});

// Loader functionality
function loader() {
    document.querySelector('.loader-container').classList.add('fade-out');
}

function fadeOut() {
    setTimeout(loader, 4500); // Executes loader fade-out once after 4.5 seconds
}

window.onload = fadeOut;
