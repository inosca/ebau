(function (window, document, undefined) {
  window.onload = init;

  function init() {
    // Ensure DOM is loaded

    let passwordIcon = document.getElementById("passwordIcon");
    let passwordConfirmIcon = document.getElementById("passwordConfirmIcon");

    let passwordInput = document.getElementById("password");
    let passwordConfirmInput = document.getElementById("password-confirm");

    // Add event listeners only if elements exist
    if (passwordIcon && passwordInput) {
      passwordIcon.addEventListener("click", function () {
        toggleShowPassword();
      });
    }

    if (passwordConfirmIcon && passwordConfirmInput) {
      passwordConfirmIcon.addEventListener("click", function () {
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
        "hidePassword"
      )
        ? "text"
        : "password";
    }

    // Center login buttons if fewer than 6 IDPs
    let iDPs = document.getElementsByClassName("button-wrapper");
    let oneClickLoginOnlyBox = document.querySelector(".one-click-login-only");
    let loginTitle = document.querySelector(".title");

    if (iDPs.length < 6 && oneClickLoginOnlyBox) {
      oneClickLoginOnlyBox.style.display = "block";
      Array.from(iDPs).forEach((idp) => {
        idp.style.margin = "auto";
        idp.style.width = "unset";
        idp.style.maxWidth = "500px";
      });
      if (loginTitle) {
        loginTitle.firstElementChild.style.textAlign = "center";
      }
    }
  }
})(window, document);
