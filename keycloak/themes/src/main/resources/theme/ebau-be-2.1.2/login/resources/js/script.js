(function(window) {
  window.onload = init;

  function init() {
    setupContactPageToggle();
    setupMobileMenuToggle();
  }
})(window);

function toggleMenu() {
  ["mobile-menu", "mobile-menu-toggle"].forEach((id) => {
    const element = document.getElementById(id);
    if (element) {
      element.classList.toggle("open");
    }
  });
}

function setupMobileMenuToggle() {
  const menuButton = document.getElementById("mobile-menu-toggle");
  if (menuButton) {
    menuButton.addEventListener("click", function() {
      toggleMenu();
    });
  }
}

/**
 * Adds history aware event listeners to all contact-box related links.
 * Which will toggle the visibilty of the contact-box and the main content.
 * */
function setupContactPageToggle() {
  const loginLinks = document.querySelectorAll(".js-login-link");
  const contactLinks = document.querySelectorAll(".js-contact-toggle");
  const mainContent = document.querySelector(".js-main-content");
  const contactBox = document.querySelector(".js-contact-box");

  function showContactBox(visible) {
    if (visible) {
      mainContent.style.display = "none";
      contactBox.style.display = "block";
      loginLinks.forEach((link) => link.classList.remove("active"));
      contactLinks.forEach((link) => {
        link.classList.add("active");
      });
    } else {
      mainContent.style.display = "block";
      contactBox.style.display = "none";
      loginLinks.forEach((link) => link.classList.add("active"));
      contactLinks.forEach((link) => {
        link.classList.remove("active");
      });
    }
  }

  // set initial history state
  history.replaceState({ contactVisible: false }, "", location.href);
  showContactBox(false);

  window.addEventListener("popstate", (event) => {
    showContactBox(event.state?.contactVisible);
  });

  [...loginLinks, ...contactLinks].forEach((link) => {
    link.addEventListener("click", function(event) {
      event.preventDefault();
      event.target.blur();

      mainContentVisible = mainContent.style.display !== "none";
      loginLinkPressed = loginLinks.values().some((e) => e === event.target);
      if (mainContentVisible !== loginLinkPressed) {
        showContactBox(mainContentVisible);
        history.pushState(
          { contactVisible: !history.state.contactVisible },
          "",
          location.href,
        );
      }
      if (this.closest("#mobile-menu")) {
        toggleMenu();
      }
    });
  });
}
