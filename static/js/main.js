// Handle file input changes
document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("resume");
  const filenameDisplay = document.getElementById("selected-filename");
  const form = document.getElementById("resume-form");
  const loading = document.getElementById("loading");

  // Handle file input changes
  if (fileInput && filenameDisplay) {
    fileInput.addEventListener("change", function () {
      if (fileInput.files.length > 0) {
        filenameDisplay.textContent = fileInput.files[0].name;
        filenameDisplay.classList.add("selected");

        // Add animation
        filenameDisplay.style.animation = "none";
        setTimeout(() => {
          filenameDisplay.style.animation = "fadeInUp 0.5s ease-out";
        }, 10);
      } else {
        filenameDisplay.textContent = "No file selected";
        filenameDisplay.classList.remove("selected");
      }
    });
  }

  // Show loading animation on form submit
  if (form && loading) {
    form.addEventListener("submit", function () {
      loading.classList.add("active");

      // Add some random progress messages to make the waiting more engaging
      const loadingMessages = [
        "Extracting resume content...",
        "Analyzing your skills...",
        "Finding educational background...",
        "Evaluating work experience...",
        "Creating personalized suggestions...",
        "Polishing the analysis...",
        "Almost done...",
      ];

      const loadingText = document.querySelector(".loading-text");
      let messageIndex = 0;

      const messageInterval = setInterval(() => {
        if (messageIndex < loadingMessages.length) {
          loadingText.textContent = loadingMessages[messageIndex];
          messageIndex++;
        } else {
          clearInterval(messageInterval);
          loadingText.textContent = "Finalizing your resume analysis...";
        }
      }, 2500);
    });
  }

  // Add scroll reveal effects
  const scrollElements = document.querySelectorAll(
    ".upload-card, .info-section, .results-container, .result-section"
  );

  const elementInView = (el, percentageScroll = 100) => {
    const elementTop = el.getBoundingClientRect().top;
    return (
      elementTop <=
      (window.innerHeight || document.documentElement.clientHeight) *
        (percentageScroll / 100)
    );
  };

  const displayScrollElement = (element) => {
    element.classList.add("scrolled");
  };

  const hideScrollElement = (element) => {
    element.classList.remove("scrolled");
  };

  const handleScrollAnimation = () => {
    scrollElements.forEach((el) => {
      if (elementInView(el, 90)) {
        displayScrollElement(el);
      } else {
        hideScrollElement(el);
      }
    });
  };

  window.addEventListener("scroll", () => {
    handleScrollAnimation();
  });

  // Initially check for elements in view
  handleScrollAnimation();
});
