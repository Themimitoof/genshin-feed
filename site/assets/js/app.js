(function () {

  function updateLanguageFilter() {
    const languageSelect = document.querySelector("select#language-selector");

    let val = languageSelect.value;
      let langsDivs = document.querySelectorAll("table.feeds-table > tbody > tr[lang]");

      if (val == "all") {
        for (lang of langsDivs) {
          lang.style.display = "";
        }
      } else {
        for (lang of langsDivs) {
          if (lang.attributes["lang"].value == val) {
            lang.style.display = "";
          } else {
            lang.style.display = "none";
          }
        }
      }
  }

  // Manage the Feeds language selector filter
  const languageSelect = document.querySelector("select#language-selector");

  if (languageSelect != null) {
    updateLanguageFilter();
    languageSelect.addEventListener("change", updateLanguageFilter);
  }
})();
