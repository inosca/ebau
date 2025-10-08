(function(window) {
  window.onload = init;

  function init() {
    setupContactPageToggle();
    setupMobileMenuToggle();
    setupPasswordInputs();
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
  const toggleLinks = document.querySelectorAll(".js-contact-toggle");
  const mainContent = document.querySelector(".js-main-content");
  const contactBox = document.querySelector(".js-contact-box");

  function showContactBox(visible) {
    if (visible) {
      mainContent.style.display = "none";
      contactBox.style.display = "block";
      loginLinks.forEach((link) => link.classList.remove("active"));
      toggleLinks.forEach((link) => {
        link.classList.add("active");
      });
    } else {
      mainContent.style.display = "block";
      contactBox.style.display = "none";
      loginLinks.forEach((link) => link.classList.add("active"));
      toggleLinks.forEach((link) => {
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

  toggleLinks.forEach((link) => {
    link.addEventListener("click", function(event) {
      event.preventDefault();
      event.target.blur();

      if (mainContent.style.display !== "none") {
        showContactBox(true);
        history.pushState({ contactVisible: true }, "", location.href);
      }
      if(this.closest("#mobile-menu")) {
        toggleMenu();
      }
    });
  });
}

function setupPasswordInputs() {
  let passwordIcon = document.getElementById("passwordIcon");
  let passwordConfirmIcon = document.getElementById("passwordConfirmIcon");

  let passwordInput = document.getElementById("password");
  let passwordConfirmInput = document.getElementById("password-confirm");

  // Add event listeners only if elements exist
  if (passwordIcon && passwordInput) {
    passwordIcon.addEventListener("click", function() {
      toggleShowPassword();
    });
  }

  if (passwordConfirmIcon && passwordConfirmInput) {
    passwordConfirmIcon.addEventListener("click", function() {
      toggleShowPasswordConfirm();
    });
  }

  function toggleShowPassword() {
    passwordIcon.classList.toggle("hidePassword");
    passwordInput.type = passwordIcon.classList.contains("hidePassword")
      ? "text"
      : "password";
  }

  function toggleShowPasswordConfirm() {
    passwordConfirmIcon.classList.toggle("hidePassword");
    passwordConfirmInput.type = passwordConfirmIcon.classList.contains(
      "hidePassword",
    )
      ? "text"
      : "password";
  }
}
