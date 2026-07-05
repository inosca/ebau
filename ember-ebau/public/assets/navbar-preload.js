// Upgrades the static navbar skeleton in index.html with the last navbar
// rendered by the Phoenix app (same-origin localStorage handoff). Runs as a
// blocking script before the Ember app boots so the navbar is present at
// first paint. The MainNavigation component removes #navbar-preload once the
// real navbar is rendered.
try {
  const nav = localStorage.getItem("ebau-navbar");
  if (nav) {
    document.getElementById("navbar-preload").innerHTML = nav;
  }
} catch {
  // localStorage unavailable (e.g. blocked by browser settings), keep skeleton
}
