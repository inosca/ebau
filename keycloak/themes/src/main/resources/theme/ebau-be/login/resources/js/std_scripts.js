function isEmpty(s) {
  return s == null || s == "undefined" || s == "";
}

function isNotEmpty(s) {
  return !isEmpty(s);
}

function isNumber(val) {
  return Number(val) == val;
}

function isValidValue(value) {
  return isNumber(value) && value >= 1 && value != '';
}

function isNotToBig(val) {
  return val.length < 5;
}

function getCookie(name)
{
var i,cname,cvalue,cookiez=document.cookie.split(";");
for (i=0;i<cookiez.length;i++)
{
  cname = cookiez[i].substr(0,cookiez[i].indexOf("="));
  cvalue = cookiez[i].substr(cookiez[i].indexOf("=")+1);
  cname = cname.replace(/^\s+|\s+$/g,"");
  if (cname==name)
    {
    return unescape(cvalue);
    }
  }
}


function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      if (oldonload) {
        oldonload();
      }
      func();
    };
  }
}

function closeDetail(elementId) {
  document.getElementById(elementId + '_Open').style.display = 'none';
  document.getElementById(elementId + '_Closed').style.display = 'block';
}

function openDetail(elementId) {
  document.getElementById(elementId + '_Open').style.display = 'block';
  document.getElementById(elementId + '_Closed').style.display = 'none';
}

function removeDivWithoutLink(element) {
  var aElements = element.getElementsByTagName('a');
  if (aElements.length == 0) {
    element.parentNode.removeChild(element);
  }
}

//'xmlhttp' request object, do not access directly, use getXmlHttp instead
var xmlhttp = null;

function getXmlHttp() {
  if (xmlhttp) {
    return xmlhttp;
    }

    if (window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
    } else if (window.ActiveXObject) {
    try {
        xmlhttp = new ActiveXObject('Msxml2.XMLHTTP');
    } catch (ex) {
        try {
        xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
        } catch (ex) {
        }
    }
    }
    return xmlhttp;
}


function sendRequest(/* String */contextPath, /* String */user,
        /* String */ pass) {
    //Warning: there is a copy of this method in /libs/cq/ui/widgets/source/User.js#login
    //changing this method means also changing User.js#login until a unique
    //and central method is implemented
    //current method is the master

    var xmlhttp = getXmlHttp();
    if (!xmlhttp) {
    return;
    }

    if (xmlhttp.readyState < 4) {
    xmlhttp.abort();
    }

    // send the authentication request
    xmlhttp.open('GET', contextPath + "?sling:authRequestLogin=1", false, user, pass);
    xmlhttp.send('');

    // check result against 403/FORBIDDEN sent by the server
    // if the credentials are wrong (other status codes like
    // 200/OK, 404/NOT FOUND or even 500/INTERNAL SERVER ERROR
    // should be considered as login success)
    return xmlhttp.status != 403;
}


function loginuser() {
    var contextPath = document.forms['login'].contextPath.value;
    var user = document.forms['login'].usr.value;
    var pass = document.forms['login'].pwd.value;
    var resource = document.forms['login'].resource.value;

    // if no user is given, avoid login request
    if (!user) {
        return false;
    }

    // send user/id password to check and persist
    if (sendRequest(contextPath, user, pass)) {

        var u = resource;
        if (window.location.hash) {
            u = u + window.location.hash;
        }
        document.location = u;

    } else {

        sendRequest(contextPath, '__failed_login_user__', 'null');

    }

    return false;
}

$(document).ready(function(event) {

    $('input[name^="anz"]').change(function() {

      // disable 'next' button
      $("#nextstep").attr("disabled", "disabled");
    // wrap price holders with loading class
    var priceHolder = $(this).parent().next();
    var currentText = $(priceHolder).text();
    $(priceHolder).text('');
        $(priceHolder).html('<span class="loading">' + currentText + '</span>');
        $("#totalSumHolder").attr("class", "loading");
        var veryTotalSum = numberize($("#cleanTotalPrice").val());

    // retrieve metadata
    var metaItems = $(this).nextAll();
    var singleItemPrice = $(metaItems).eq(0).val();
    var numberOfFreeCopies = $(metaItems).eq(1).val();
    var currency = $(metaItems).eq(2).val();

    var prevNumber = $(metaItems).eq(3);

    // perform calculation
    var numberOfItems = $(this).val();

    if (isValidValue(numberOfItems)) {
                  $("p.invalidnumber").hide("fast");
                  $(this).removeClass('error');
                }

                if (isNotToBig(numberOfItems)) {
                  $("p.bignumber").hide("fast");
                  $(this).removeClass('error');
                }

                if (!isValidValue(numberOfItems) || !isNotToBig(numberOfItems)) {
                        if (!isValidValue(numberOfItems)) {
                          $("p.invalidnumber").show("fast");
                        }
                        if (!isNotToBig(numberOfItems)) {
                          $("p.bignumber").show("fast");
                        }
                        $(this).addClass('error');
                }

    var oldPrice = calculatePrice($(prevNumber).val(), numberOfFreeCopies, singleItemPrice);
    var newPrice = calculatePrice(numberOfItems, numberOfFreeCopies, singleItemPrice);


    // set new values, remove loading class, enable 'next' button
    $(prevNumber).val(numberOfItems);
    $(priceHolder).html(formatCurrency(newPrice));
    var newVeryTotal = veryTotalSum + newPrice - oldPrice;
    $("#totalSumHolder").text(formatCurrency(newVeryTotal));
    $("#totalSumHolder").removeAttr("class");
    $("#cleanTotalPrice").val(formatCurrency(newVeryTotal));
    $("#nextstep").removeAttr("disabled");
    });

    $("form#warenkorbstep1").submit(function() {
      var dosubmit = true;
      $('input[name^="anz"]').each(function() {
        dosubmit = dosubmit && isValidValue($(this).val());
      });
      return dosubmit;
    });
});

function calculatePrice(numberOfItems, freeCopies, pricePerItem) {

  var factor = 0;
  if (isNumber(numberOfItems)) {
    factor = numberOfItems;
  }

  var newPrice = pricePerItem * (factor - freeCopies);

  return newPrice > 0 ? newPrice : 0;
}

function formatCurrency(value) {
  var fPrice = '';
  var newValue = value.toFixed(2);
  var len = newValue.length;
  var offset = (len-3) % 3;
  if ((len-3) <= 3) {
    return newValue;
  } else {
    for(i = len - 6; i >= offset; i -= 3) {
      if (i==len-6) {
        fPrice = newValue.substring(i, newValue.length);
      } else {
        fPrice = newValue.substring(i, i+3) + "'" + fPrice;
      }
    }

    fPrice = newValue.substring(0, offset) + "'" + fPrice;

    if (fPrice.substring(0,1) == "'") {
      fPrice = fPrice.substring(1, fPrice.length);
    }
  }

  return fPrice;
}

function numberize(num) {
  var number = num + "";
  var number = number.replace("'", "");
  return Number(number);
}

function getDateFromElement(elementId) {
    var rawDate = document.getElementById(elementId).value;
    if (rawDate != "") {
        var dateParts = rawDate.split(".");
        var year = dateParts[2];
        var month = dateParts[1] - 1; //the month in javascript is coded from 0 to 11
        var day = dateParts[0];

        var fourDigitYear;
        if (year.length == 2) {
            //Date() in javascript interpret year 00 as year 1900 instead of 2000
            //hence we convert it to 4-digits
            fourDigitYear = parseInt(year) + 2000;
        } else {
            fourDigitYear = year;
        }

        return new Date(fourDigitYear, month, day);
    }
    return "";
}

/**
 * Check if first is before second
 */
function dateIsBefore(first, second) {
  if (!isEmpty(first) && first != NaN) {
    if (!isEmpty(second) && second != NaN) {
      return first.getTime() < second.getTime();
    }
    return true;
  }
  return true;
}

/**
 * Check if first is after second
 */
function dateIsAfter(first, second) {
  if (!isEmpty(first) && first != NaN) {
    if (!isEmpty(second) && second != NaN) {
      return first.getTime() > second.getTime();
    }
    return true;
  }
  return true;
}

/**
 * Check if first is no later than second
 */
function dateIsNoLater(first, second) {
    if (!isEmpty(first) && first != NaN) {
        if (!isEmpty(second) && second != NaN) {
            return first.getTime() <= second.getTime();
        }
        return true;
    }
    return true;
}