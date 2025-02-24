document.addEventListener("DOMContentLoaded", function () {
    const userIcons = document.querySelectorAll(".dropdown-user, .dropdown-in");
    
    userIcons.forEach((container) => {
      const trigger = container.querySelector(".user-icon");
      const dropdown = container.querySelector(".custom-dropdown");
  
      trigger.addEventListener("click", function (e) {
        e.preventDefault();
        // Toggle dropdown visibility
        if (dropdown.style.display === "block") {
          dropdown.style.display = "none";
        } else {
          // Hide any other open dropdowns
          document.querySelectorAll(".custom-dropdown").forEach((dd) => {
            dd.style.display = "none";
          });
          dropdown.style.display = "block";
        }
      });
  
      // Close dropdown if clicking outside
      document.addEventListener("click", function (e) {
        if (!container.contains(e.target)) {
          dropdown.style.display = "none";
        }
      });
    });
  });
  