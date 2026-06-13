/**
 * Front-end Scripts for Expense Tracker Pro
 */

// Modal utilities
function openEditModal(txId, description, amount, category, date) {
  const modal = document.getElementById("editModal");
  const form = document.getElementById("editForm");

  // Dynamically set form submission path
  form.action = `/transactions/${txId}/edit`;

  // Pre-fill fields
  document.getElementById("edit_description").value = description;
  document.getElementById("edit_amount").value = amount;
  document.getElementById("edit_category").value = category;

  if (date) {
    document.getElementById("edit_date").value = date;
  }

  modal.style.display = "flex";
}

function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
}

// Close modal if user clicks on overlay backdrop
window.addEventListener("click", (e) => {
  const modal = document.getElementById("editModal");
  if (e.target === modal) {
    closeEditModal();
  }
});

// Show & pre-fill the Other Income form when a quick button is clicked
function fillOtherIncome(type) {
  const form = document.getElementById("otherIncomeForm");
  const descInput = document.getElementById("income_description");
  const dateInput = document.getElementById("income_date");

  form.style.display = "block";
  form.scrollIntoView({ behavior: "smooth", block: "nearest" });

  if (descInput) {
    descInput.value = type;
    descInput.focus();
    // Trigger live detection badge
    descInput.dispatchEvent(new Event("input"));
  }
  if (dateInput && !dateInput.value) {
    dateInput.value = new Date().toLocaleDateString("en-CA");
  }
}

// Setup Page Elements
document.addEventListener("DOMContentLoaded", () => {
  const descInput = document.getElementById("description");
  const catSelect = document.getElementById("category");
  const badge = document.getElementById("detector-badge");
  const detectedSpan = document.getElementById("detected-cat");

  // Pre-fill creation date with current local date
  const dateInput = document.getElementById("date");
  if (dateInput && !dateInput.value) {
    const today = new Date().toLocaleDateString("en-CA"); // Formats to YYYY-MM-DD
    dateInput.value = today;
  }

  // Live Category Auto-Detection
  if (descInput && catSelect && badge && detectedSpan) {
    let debounceTimer = null;

    const queryCategoryDetection = async () => {
      const descriptionText = descInput.value.trim();

      // Only run if description has substance and category selection is set to 'Auto'
      if (descriptionText.length >= 2 && catSelect.value === "Auto") {
        try {
          const response = await fetch("/api/transactions/detect", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json",
            },
            body: JSON.stringify({ description: descriptionText }),
          });

          if (response.ok) {
            const data = await response.json();
            detectedSpan.textContent = data.category;
            badge.classList.add("visible");
          } else {
            badge.classList.remove("visible");
          }
        } catch (error) {
          console.error("Failed to fetch live category auto-detection:", error);
          badge.classList.remove("visible");
        }
      } else {
        badge.classList.remove("visible");
      }
    };

    descInput.addEventListener("input", () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(queryCategoryDetection, 350); // 350ms debounce
    });

    catSelect.addEventListener("change", () => {
      if (catSelect.value === "Auto") {
        queryCategoryDetection();
      } else {
        badge.classList.remove("visible");
      }
    });
  }

  // ── Income Panel: pre-fill today's date for salary & other income ────────
  const salaryDateInput = document.getElementById("salary_date");
  if (salaryDateInput && !salaryDateInput.value) {
    salaryDateInput.value = new Date().toLocaleDateString("en-CA");
  }

  // ── Income Panel: Live source detection badge ─────────────────────────────
  const incomeDescInput = document.getElementById("income_description");
  const incomeBadge     = document.getElementById("income-badge");
  const incomeDetected  = document.getElementById("income-detected-cat");

  const incomeSourceLabels = {
    "Salary / Income": "Salary / Income",
    "Food & Drinks":   "Food (unusual?)",
    "Transport":       "Transport",
    "Other":           "General Income",
  };

  if (incomeDescInput && incomeBadge && incomeDetected) {
    let incomeDebounce = null;

    const queryIncomeSource = async () => {
      const text = incomeDescInput.value.trim();
      if (text.length >= 2) {
        try {
          const res = await fetch("/api/transactions/detect", {
            method: "POST",
            headers: { "Content-Type": "application/json", "Accept": "application/json" },
            body: JSON.stringify({ description: text }),
          });
          if (res.ok) {
            const data = await res.json();
            incomeDetected.textContent = incomeSourceLabels[data.category] || data.category;
            incomeBadge.classList.add("visible");
          }
        } catch (e) {
          incomeBadge.classList.remove("visible");
        }
      } else {
        incomeBadge.classList.remove("visible");
      }
    };

    incomeDescInput.addEventListener("input", () => {
      clearTimeout(incomeDebounce);
      incomeDebounce = setTimeout(queryIncomeSource, 350);
    });
  }

  // Auto-dismiss alert boxes after 5 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.5s ease, transform 0.5s ease";
      alert.style.opacity = "0";
      alert.style.transform = "translateY(-10px)";
      setTimeout(() => {
        alert.remove();
      }, 500);
    }, 5000);
  });
});
