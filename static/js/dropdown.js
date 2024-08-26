document.addEventListener("DOMContentLoaded", function() {
    const dropdownToggleLinks = document.querySelectorAll(".dropdown-toggle");

    dropdownToggleLinks.forEach(function(link) {
        link.addEventListener("mouseover", function() {
            closeAllDropdowns();
            this.nextElementSibling.style.display = "block";
        });
    });

    function closeAllDropdowns() {
        const dropdownMenus = document.querySelectorAll(".dropdown-menu");
        dropdownMenus.forEach(function(menu) {
            menu.style.display = "none";
        });
    }
});