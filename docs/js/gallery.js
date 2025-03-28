document.addEventListener('DOMContentLoaded', function() {
    const slidesContainer = document.querySelector('.slides-container');
    const slides = document.querySelectorAll('.slide');
    const dotsContainer = document.querySelector('.dots-container');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    let currentIndex = 0;
    let slidesPerView = getSlidesPerView();
    
    // Create navigation dots
    slides.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        if (index === currentIndex) dot.classList.add('active');
        dot.addEventListener('click', () => goToSlide(index));
        dotsContainer.appendChild(dot);
    });
    
    const dots = document.querySelectorAll('.dot');
    
    // Update the number of slides per view based on window size
    function getSlidesPerView() {
        return window.innerWidth >= 768 ? 3 : 1;
    }
    
    // Go to slide
    function goToSlide(index) {
        // Mobile (1 slide)
        if (slidesPerView === 1) {
            currentIndex = index;
            slidesContainer.scrollTo({
                left: slides[index].offsetLeft,
                behavior: 'smooth'
            });
        } 
        // Desktop (5 slides)
        else {
            currentIndex = index;
            const scrollPosition = index === 0 ? 0 : slides[index].offsetLeft - slidesContainer.offsetWidth / 3;
            slidesContainer.scrollTo({
                left: scrollPosition,
                behavior: 'smooth'
            });
        }
        
        updateDots();
    }
    
    // Update dots
    function updateDots() {
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentIndex);
        });
    }
    
    // Go to previous graph
    function prevSlide() {
        if (currentIndex > 0) {
            goToSlide(currentIndex - 1);
        } else {
            goToSlide(slides.length - 1);
        }
    }
    
    // Go to next graph
    function nextSlide() {
        if (currentIndex < slides.length - 1) {
            goToSlide(currentIndex + 1);
        } else {
            goToSlide(0);
        }
    }
    
    // Event listeners
    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);
    
    // Resize window
    window.addEventListener('resize', function() {
        slidesPerView = getSlidesPerView();
        goToSlide(currentIndex);
    });
    
    // Initialize
    goToSlide(0);
});