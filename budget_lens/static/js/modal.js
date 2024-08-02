document.addEventListener("DOMContentLoaded", (event) => {
    var settings = document.getElementById("settings-modal");
    var openModalBtn = document.getElementById("openModalBtn");

    openModalBtn.onclick = function() {
        settings.style.display = "block";
    }

    var closeButtons = document.querySelectorAll(".close-modal");
    closeButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            closeModalWithAnimation();
        });
    });

    window.onclick = function(event) {
        if (event.target == settings) {
            closeModalWithAnimation();
        }
    }

    function closeModalWithAnimation() {
        settings.style.display = "none";

        openModalBtn.classList.add("rotate");

        setTimeout(function() {
            openModalBtn.classList.remove("rotate");
        }, 1000);
    }
});
