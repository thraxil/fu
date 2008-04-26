function showAuthorBio() {
  var id = this.href.split("#")[1];
  showElement(id);
  return false;
  }

function initAuthorPopup(element) {
  element.onclick = showAuthorBio;
  }

function initAuthorCloseLink(element) {
  element.onclick = closeAuthorBio;
  }

function closeAuthorBio() {
  var id = this.href.split("#")[1];
  hideElement(id);
  return false;
  }

function initBioPopups() {
  forEach(getElementsByTagAndClassName("a","author-link"),
	  initAuthorPopup);
  forEach(getElementsByTagAndClassName("a","close-link"),
	  initAuthorCloseLink);
  }

addLoadEvent(initBioPopups);
