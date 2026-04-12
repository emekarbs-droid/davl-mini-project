function openTab(evt, tabName) {
    // Get all elements with class="tab-content" and hide them
    var tabcontent = document.getElementsByClassName("tab-content");
    for (var i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        tabcontent[i].classList.remove("active");
    }

    // Get all elements with class="tab-link" and remove the class "active"
    var tablinks = document.getElementsByClassName("tab-link");
    for (var i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    var activeTab = document.getElementById(tabName);
    activeTab.style.display = "block";
    
    // Slight delay to allow display to register before triggering opacity animation via class addition
    setTimeout(() => {
        activeTab.classList.add("active");
    }, 10);
    
    evt.currentTarget.classList.add("active");

    // Re-trigger Plotly resize events in case graphs were rendered off-screen
    window.dispatchEvent(new Event('resize'));
}

// Optionally, add a loading state check
document.addEventListener("DOMContentLoaded", function() {
    var submitBtn = document.getElementById("submitBtn");
    var fileInput = document.getElementById("fileInput");

    if (submitBtn && fileInput) {
        submitBtn.addEventListener("click", function(e) {
            if (fileInput.files.length > 0) {
                submitBtn.innerText = "Processing Data...";
                submitBtn.style.opacity = "0.7";
                submitBtn.disabled = true;
                
                // Submit form after logic
                submitBtn.closest('form').submit();
            }
        });
    }
});
