(function() {
  try {
    var cache = localStorage.getItem('ebau-nav-cache');
    if (cache) {
      var nav = document.getElementById('initial-loader');
      if (nav) {
        nav.innerHTML = cache;
      }
    }
  } catch (e) {
    console.warn('Failed to restore navbar cache', e);
  }
})();