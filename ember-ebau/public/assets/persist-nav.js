(function () {
  const saveNav = function () {
    try {
      // Find all navigations, but ignore the skeleton loader
      const navs = document.querySelectorAll(
        ".main-navigation:not(#initial-loader)",
      );
      // The real one is likely the last one or the only one left visible
      const nav = navs.length > 0 ? navs[navs.length - 1] : null;

      // Only save if the navbar has actual items (not just the skeleton)
      if (nav && nav.querySelectorAll("li").length > 1) {
        localStorage.setItem("ebau-nav-cache", nav.innerHTML);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Periodically check for updates during the first 20 seconds of session
  // to capture data-driven changes in the navigation.
  window.addEventListener("load", function () {
    let count = 0;
    const interval = setInterval(function () {
      saveNav();
      if (++count > 10) clearInterval(interval);
    }, 2000);
  });

  // Ensure we capture the final state before the user leaves
  window.addEventListener("beforeunload", saveNav);
})();
