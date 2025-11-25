// API base URL
const API_URL = "";

// State
let statusCheckInterval = null;

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  loadStats();
  loadLeads();

  // Set up form submission
  document
    .getElementById("scrapingForm")
    .addEventListener("submit", startScraping);

  // Set up filters
  document.getElementById("filterType").addEventListener("change", loadLeads);
  document
    .getElementById("searchInput")
    .addEventListener("input", debounce(loadLeads, 500));
});

// Start scraping
async function startScraping(e) {
  e.preventDefault();

  const niche = document.getElementById("niche").value;
  const location = document.getElementById("location").value;
  const maxPages = document.getElementById("maxPages").value;

  const startBtn = document.getElementById("startBtn");
  startBtn.disabled = true;
  startBtn.innerHTML = "<span>⏳ Scraping...</span>";

  const progressContainer = document.getElementById("progressContainer");
  progressContainer.style.display = "block";

  try {
    const response = await fetch(`${API_URL}/api/start-scraping`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ niche, location, max_pages: maxPages }),
    });

    const data = await response.json();

    if (response.ok) {
      // Start checking status
      statusCheckInterval = setInterval(checkScrapingStatus, 1000);
    } else {
      alert("Error: " + data.error);
      resetScrapingUI();
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to start scraping");
    resetScrapingUI();
  }
}

// Check scraping status
async function checkScrapingStatus() {
  try {
    const response = await fetch(`${API_URL}/api/status`);
    const status = await response.json();

    // Update progress bar
    document.getElementById("progressFill").style.width = status.progress + "%";
    document.getElementById("progressText").textContent = status.message;

    // If scraping is complete
    if (!status.is_running && statusCheckInterval) {
      clearInterval(statusCheckInterval);
      statusCheckInterval = null;

      setTimeout(() => {
        resetScrapingUI();
        loadStats();
        loadLeads();
      }, 2000);
    }
  } catch (error) {
    console.error("Error checking status:", error);
  }
}

// Reset scraping UI
function resetScrapingUI() {
  const startBtn = document.getElementById("startBtn");
  startBtn.disabled = false;
  startBtn.innerHTML = "<span>Start Scraping</span>";

  document.getElementById("progressContainer").style.display = "none";
  document.getElementById("progressFill").style.width = "0%";
}

// Load statistics
async function loadStats() {
  try {
    const response = await fetch(`${API_URL}/api/stats`);
    const stats = await response.json();

    document.getElementById("totalLeads").textContent = stats.total;
    document.getElementById("noWebsiteLeads").textContent = stats.no_website;
    document.getElementById("withWebsiteLeads").textContent = stats.has_website;
  } catch (error) {
    console.error("Error loading stats:", error);
  }
}

// Load leads
async function loadLeads() {
  const filterType = document.getElementById("filterType").value;
  const search = document.getElementById("searchInput").value;

  try {
    const response = await fetch(
      `${API_URL}/api/leads?filter=${filterType}&search=${encodeURIComponent(
        search
      )}`
    );
    const leads = await response.json();

    displayLeads(leads);
  } catch (error) {
    console.error("Error loading leads:", error);
  }
}

// Display leads in table
function displayLeads(leads) {
  const tbody = document.getElementById("leadsTableBody");

  if (leads.length === 0) {
    tbody.innerHTML = `
            <tr>
                <td colspan="6" class="empty-state">
                    No leads found. Try adjusting your filters or start a new search.
                </td>
            </tr>
        `;
    return;
  }

  tbody.innerHTML = leads
    .map(
      (lead) => `
        <tr>
            <td><strong>${escapeHtml(lead.name)}</strong></td>
            <td>${escapeHtml(lead.category)}</td>
            <td>${escapeHtml(lead.phone)}</td>
            <td>${escapeHtml(lead.address)}</td>
            <td>
                ${
                  lead.has_website
                    ? `<a href="${escapeHtml(
                        lead.website
                      )}" target="_blank" class="website-link">Visit</a>`
                    : `<span class="website-badge no-website">No Website</span>`
                }
            </td>
            <td>
                <button class="btn-delete" onclick="deleteLead(${
                  lead.id
                })">Delete</button>
            </td>
        </tr>
    `
    )
    .join("");
}

// Delete lead
async function deleteLead(id) {
  if (!confirm("Are you sure you want to delete this lead?")) {
    return;
  }

  try {
    const response = await fetch(`${API_URL}/api/delete-lead/${id}`, {
      method: "DELETE",
    });

    if (response.ok) {
      loadStats();
      loadLeads();
    } else {
      alert("Failed to delete lead");
    }
  } catch (error) {
    console.error("Error deleting lead:", error);
    alert("Failed to delete lead");
  }
}

// Export leads
async function exportLeads() {
  try {
    window.location.href = `${API_URL}/api/export`;
  } catch (error) {
    console.error("Error exporting leads:", error);
    alert("Failed to export leads");
  }
}

// Clear all leads
async function clearAllLeads() {
  if (
    !confirm(
      "Are you sure you want to delete ALL leads? This cannot be undone!"
    )
  ) {
    return;
  }

  try {
    const response = await fetch(`${API_URL}/api/clear-all`, {
      method: "POST",
    });

    if (response.ok) {
      loadStats();
      loadLeads();
    } else {
      alert("Failed to clear leads");
    }
  } catch (error) {
    console.error("Error clearing leads:", error);
    alert("Failed to clear leads");
  }
}

// Utility functions
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}
