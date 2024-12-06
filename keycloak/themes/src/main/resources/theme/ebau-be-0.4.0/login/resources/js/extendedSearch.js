/*

KTBE Mobile
Lieferung v. 9.1.2015
Release 4.1
Fix Version 4.1.1


*/


function submitSearchForm(li) {
  $('input#form-keyword').val($(li).text());
  $("input#gsa-submit").click();
}


function submitHeaderSearchForm(li) {
  $('input#ext-searchform-keyword').val($(li).text());
  $("form#ext-search").submit();
}

function createHeaderAutocomplete(url, charLength, boxHeight) {
  // KTBE-5814 - reduced animation duration + timeout
  $(document).ready(function() {
    $('#search').click(function(){
      $('#id-ext-search').css('display','block');
      $('#id-ext-search').animate({ width: 500 }, 10, function(){});
      $('#id-ext-search').animate({ height: boxHeight }, 200, function(){});
      setTimeout(function() {
        $('#ext-searchform-keyword').focus();
        //timeout added, as a fix for KTBE-4694
      }, 20); // 500
    })
    $('a.closeext').click(function(e) {
      e.preventDefault();
      $('#id-ext-search').animate({ height: 0 }, 200, function(){});
      $('#id-ext-search').animate({ width: 0 }, 20, function(){});

      setTimeout(function(){
          $('#id-ext-search').css('display','none');
        }, 70 );
    })

    //define header's autocomplete
    var a = $('#ext-searchform-keyword').autocomplete({
      source: url,
      minLength: charLength,
      appendTo: '#suggestions_top'
    });
    //override to remove plugin's specific style
    a.data("ui-autocomplete")._suggest = function(items) {
      var ul = this.menu.element
        .empty()
        .zIndex( this.element.zIndex() + 1 );
      this._renderMenu( ul, items );
      this.menu.refresh();
      ul.removeAttr("class");
      ul.addClass("ss-gac blind");
      ul.removeAttr("style");
      ul.show();
    };
    //override to define html according to prototype
    a.data("ui-autocomplete")._renderItem = function(ul, item) {
      return $( "<li onclick='submitHeaderSearchForm(this)'>")
      .data( "item.autocomplete", item )
      .append( $( "<a class='gsaSuggestion'></a>" ).text(item.label))
      .appendTo( ul );
    };
    $("#ext-searchform-keyword").keyup(function() {
      if ($(this).val().length >= charLength) {
        $('#search_suggest_top').css('display','block');
        $('.schliessen').css('display','none');
      }
    });
    $('#closesugtop').click(function(e){
      e.preventDefault();
      $('#search_suggest_top').css('display','none');
      $('.schliessen').css('display','block');
    });
  });
}

function createSucheAutocomplete(url, charLength) {
  $(document).ready(function(){

    var b = $('#form-keyword').autocomplete({
      source: url,
      minLength: charLength,
      appendTo: '#suggestions'
    });
    b.data("ui-autocomplete")._suggest = function(items) {
      var ul = this.menu.element
        .empty()
        .zIndex( this.element.zIndex() + 1 );
      this._renderMenu( ul, items );
      this.menu.refresh();
      ul.removeAttr("class");
      ul.addClass("ss-gac blind");
      ul.removeAttr("style");
      ul.show();
    };
    b.data("ui-autocomplete")._renderItem = function(ul, item) {
      return $("<li onclick='submitSearchForm(this)'></li>")
      .data( "item.autocomplete", item)
      .append($("<a class='gsaSuggestion'></a>").text(item.label))
      .appendTo(ul);
    };

    $("#form-keyword").keyup(function() {
      if ($(this).val().length >= charLength) {
        $('#search_suggest').css('display', 'block');
      }
    });

    $('#closesug').click(function() {
      $('#search_suggest').css('display', 'none');
    });

  });
}