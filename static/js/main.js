// Handle file input changes
document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("resume");
  const filenameDisplay = document.getElementById("selected-filename");

  if (fileInput && filenameDisplay) {
    fileInput.addEventListener("change", function () {
      if (fileInput.files.length > 0) {
        filenameDisplay.textContent = fileInput.files[0].name;
      } else {
        filenameDisplay.textContent = "No file selected";
      }
    });
  }
});
