/**
 * Delete item from the basket.
 * If javascript is enabled item is deleted via ajax GET method
 * otherwise given url is just opened(specified as href attrbute od <a> tag)
 * 
 * @param item - item that need to be deleted
 * @param message - confirmation message that need to be shown
 * @param url - url called by ajax GET method
 * @param reload - flag that force page reload when link is successfully deleted.
 *      It is useful when we are sure that all our visitor browsers support javascript
 *      so we can prevent page reload by setting reload parameter to "false"
 *      (item will be deleted by ajax call and removed from table by javascript).
 */
function deleteBasketItem(item, message, url, reload) {
    var answer = confirm(message);
    if (answer) {
        //if answer is 'yes'
        if (!reload) {
             // dont reload page + ajax delete
             $.ajax({
              url: url,
              success: function() {
                  var parentRow = item.parentNode.parentNode;
                  var parentTable = parentRow.parentNode;
                  parentTable.removeChild(parentRow);
              }
            });
        }
    } else {
        reload = false;
    }
    return reload;
}

function showFieldset(elem) {
	  elem.parent().parent().parent().parent().show("fast");
}

function hideFieldset(elem) {
	  elem.parent().parent().parent().parent().hide("fast");
}