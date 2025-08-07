//   <!-- JS for Modal -->
function openModal() {
  document.getElementById("modal").style.display = "flex";
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
}

// Close modal if clicked outside the modal box
window.addEventListener("click", function (e) {
  const modal = document.getElementById("modal");
  if (e.target === modal) {
    closeModal();
  }
});

// for opensource section
function openOpenSourceModal() {
  document.getElementById("openSourceModalOverlay").style.display = "flex";
}

function closeOpenSourceModal() {
  document.getElementById("openSourceModalOverlay").style.display = "none";
}

// Close when clicking outside modal
window.addEventListener("click", function (e) {
  const modal = document.getElementById("openSourceModalOverlay");
  if (e.target === modal) {
    closeOpenSourceModal();
  }
});

// fot toast message
function showPricingToast() {
  const toastElement = document.getElementById("pricingToast");
  const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
  toast.show();
}
