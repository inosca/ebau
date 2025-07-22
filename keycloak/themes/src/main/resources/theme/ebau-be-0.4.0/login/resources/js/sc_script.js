
/*

KTBE Mobile
Lieferung v. 9.1.2015
Release 4.1
Fix Version 4.1.1


*/


// Zeigt den Gemeinden-Selektor an
function show_selector(title) {
  'use strict';

  $('#'+title+' .commune-selector').removeClass('required');
  $('#'+title+' .commune-selector').show();
}

// Ubernimmt die gewahlte Gemeinde und blendet den Gemeinden-Selektor sowie die Liste aus
function select_commune(o, changeCommuneString, clearCommuneString, title) {
  'use strict';

  $('#'+title+' .commune-current').remove();
  var c = $('label[for="'+o+'"]').html();


  //$('#'+title+' .commune-widget').before('<div class="commune-current" aria-live="polite">' + c + ' <a href="#" onclick="show_selector(\''+title+'\'); return false">' + changeCommuneString + '</a> <a href="#" onclick="clear_selection(\''+title+'\'); return false">' + clearCommuneString + '</a></div>');
  $('#'+title+' .commune-widget').before('<div class="commune-current" aria-live="polite">' + c + ' <a href="#' +title+'" onclick="show_selector(\''+title+'\');">' + changeCommuneString + '</a> <a href="#'+title+'" onclick="clear_selection(\''+title+'\');">' + clearCommuneString + '</a></div>');

  $('#'+title+' #'+o).attr('checked','checked');
  $('#'+title+' .commune-selector').hide();
  $('#'+title+' .commune-list').hide();
  $('body').scrollTop(0); // KTBE-5880
}

function clear_selection(title) {
  'use strict';

  $('#'+title+' .commune-current').remove();
  $('#'+title+' input:checked').removeAttr('checked');
  show_selector(title);
}

function renderCommuneSelector(name, changeCommuneString, clearCommuneString, title, additionalClass) {
  'use strict';

  // Layers verstecken
  $('#'+title+' .commune-list div').css('display','none');

  // Klick-Control
  $(document).on('click', '#'+title+' .commune-selector a', function(e) {
    //e.preventDefault();
    $('#'+title+' .commune-list').show();
    $('#'+title+' .commune-list div').css('display','none');
    $('#'+title+' .commune-list div').attr('aria-hidden','true');
    $('#'+name+'-list-'+$(this).html()).css('display','block');
    $('#'+name+'-list-'+$(this).html()).attr('aria-hidden','false');
    //return false;
  });

  // Radiobuttons entfernen
  $('#'+title+' .commune-list input').hide();

  // ABC-Layer einfugen
  var cse = '<div class="abc commune-selector ' + additionalClass + '" role="tablist"><ul>';
  var abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var char, exists;
  for (var i = 0; i < abc.length; i++) {
    char   = abc.charAt(i);
    exists = $('#'+name+'-list-'+char).size()>0;
    cse += '<li>';
    if (exists) {
      cse += '<a role="tab" id="aria-tab-'+char+'" href="#'+name+'-list-'+char+'">';
    } else {
      cse += '<span>';
    }
    cse += char;
    if (exists) {
      cse += '</a>';
    } else {
      cse += '</span>';
    }
    cse += '</li>';
  }
  cse += '</ul></div>';
  $('#'+title+' .commune-widget').prepend(cse);

  // Anker fur vorhandene Gemeinden erstellen
  $('#'+title+' .commune-list label').each(function(){
    $(this).wrap('<a href="#" onclick="select_commune(\''+$(this).attr('for')+'\',\''+ changeCommuneString +'\', \'' + clearCommuneString + '\', \'' + title + '\'); return false"></a>');
  });

  // Gemeinde bereits gewahlt? Dann aktuelle Gemeinde einblenden
  if($('input[name="' + name + '"]:checked').attr('id')) {
    select_commune($('input[name="' + name + '"]:checked').attr('id'), changeCommuneString, clearCommuneString, title);
  }

  // ARIA
  $('#'+title+' .commune-widget').attr('role', 'tabpanel');
  $('#'+title+' .commune-widget').attr('aria-live', 'polite');
  $('#'+title+' .commune-list').attr('aria-live', 'polite');
  $('#'+title+' .commune-list div').attr('role', 'tabpanel');
  $('#'+title+' .commune-list div').each(function(){
    var id = $(this).attr('id').match(/[A-Z]{1}/);
    $('#'+name+'-list-'+id).attr('aria-labelledby', 'aria-tab-'+id);
  });
}
