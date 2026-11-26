document.addEventListener("DOMContentLoaded", () => {
    const slidesContainer = document.querySelector(".slides-container");
    const slides = Array.from(document.querySelectorAll(".slide"));
    const dotsContainer = document.querySelector(".dots-container");
    const previousButton = document.querySelector(".prev-btn");
    const nextButton = document.querySelector(".next-btn");

    if (!slidesContainer || !dotsContainer || !previousButton || !nextButton || slides.length === 0) {
        return;
    }

    let currentIndex = 0;
    let slidesPerView = window.innerWidth >= 768 ? 3 : 1;

    const dots = slides.map((slide, index) => {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "dot";
        dot.setAttribute("aria-label", `Show chart ${index + 1}`);
        dot.addEventListener("click", () => goToSlide(index));
        dotsContainer.appendChild(dot);
        return dot;
    });

    function goToSlide(index) {
        currentIndex = index;
        const scrollPosition = slidesPerView === 1 || index === 0
            ? slides[index].offsetLeft
            : slides[index].offsetLeft - slidesContainer.offsetWidth / 3;

        slidesContainer.scrollTo({ left: scrollPosition, behavior: "smooth" });
        dots.forEach((dot, dotIndex) => {
            dot.classList.toggle("active", dotIndex === currentIndex);
            dot.setAttribute("aria-current", dotIndex === currentIndex ? "true" : "false");
        });
    }

    previousButton.addEventListener("click", () => {
        goToSlide(currentIndex === 0 ? slides.length - 1 : currentIndex - 1);
    });
    nextButton.addEventListener("click", () => {
        goToSlide(currentIndex === slides.length - 1 ? 0 : currentIndex + 1);
    });

    window.addEventListener("resize", () => {
        slidesPerView = window.innerWidth >= 768 ? 3 : 1;
        goToSlide(currentIndex);
    });

    goToSlide(currentIndex);
});
