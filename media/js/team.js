function showAuthorBio() {
  var id = this.href.split("#")[1];
  makeVisible(id);
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
  makeInvisible(id);
  return false;
  }

function initBioPopups() {
  forEach(getElementsByTagAndClassName("a","author-link"),
	  initAuthorPopup);
  forEach(getElementsByTagAndClassName("a","close-link"),
	  initAuthorCloseLink);
  }


   function toggleVisible(elem) {
        toggleElementClass("invisible", elem);
    }

    function makeVisible(elem) {
        removeElementClass(elem, "invisible");
    }

    function makeInvisible(elem) {
        addElementClass(elem, "invisible");
    }

    function isVisible(elem) {
        // you may also want to check for
        // getElement(elem).style.display == "none"
        return !hasElementClass(elem, "invisible");
    };


addLoadEvent(initBioPopups);
