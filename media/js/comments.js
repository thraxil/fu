
function commentSubmit() {

  var content = document.getElementById("comment-textarea").value;
  var name = document.getElementById("comment-name").value;
  var email = document.getElementById("comment-email").value;
  var url = document.getElementById("comment-url").value;

  if (content == "") {
    alert("your comment is empty.");
    return false;
  }

  if (name == "") {
    alert("you need to enter a name.");
    return false;
  }

  if (email == "") {
    alert("you need to enter an email address (it won't be shown)");
    return false;
  }

  var remember = document.getElementById("comment-remember");

  var now = new Date();
  fixDate(now);
  now.setTime(now.getTime() + 365 * 24 * 60 * 60 * 1000);

  if (remember.checked) {
    setCookie('name', name, now, '/', '', '');
    setCookie('email', email, now, '/', '', '');
    setCookie('url', url, now, '/', '', '');
    setCookie("remember","remember",now,'/','','')
  } else {
    deleteCookie('name','/','');
    deleteCookie('email','/','');
    deleteCookie('url','/','');
    setCookie('remember',"forget",now,'/','','');
  }

  return true;
  }


function setCookie (name, value, expires, path, domain, secure) {
    var curCookie = name + "=" + escape(value) + ((expires) ? "; expires=" + expires.toGMTString() : "") + ((path) ? "; path=" + path : "") + ((domain) ? "; domain=" + domain : "") + ((secure) ? "; secure" : "");
    document.cookie = curCookie;
}

function getCookie (name) {
    var prefix = name + '=';
    var c = document.cookie;
    var nullstring = '';
    var cookieStartIndex = c.indexOf(prefix);
    if (cookieStartIndex == -1)
        return nullstring;
    var cookieEndIndex = c.indexOf(";", cookieStartIndex + prefix.length);
    if (cookieEndIndex == -1)
        cookieEndIndex = c.length;
    return unescape(c.substring(cookieStartIndex + prefix.length, cookieEndIndex));
}

function deleteCookie (name, path, domain) {
    if (getCookie(name))
        document.cookie = name + "=" + ((path) ? "; path=" + path : "") + ((domain) ? "; domain=" + domain : "") + "; expires=Thu, 01-Jan-70 00:00:01 GMT";
}

function fixDate (date) {
    var base = new Date(0);
    var skew = base.getTime();
    if (skew > 0)
        date.setTime(date.getTime() - skew);
}

window.onload = function () {
  var remember = getCookie('remember');
  var name = document.getElementById('comment-name');
  if (!name) {
    return; // no comment form on page
  }
  document.getElementById('comment-name').value = getCookie('name');
  document.getElementById('comment-email').value = getCookie('email');
  document.getElementById('comment-url').value = getCookie('url');
  if (remember == "remember") {
    document.getElementById('comment-remember').checked = true;
  }
  if (remember == "forget") {
    document.getElementById('comment-remember').checked = false;
  }
}
