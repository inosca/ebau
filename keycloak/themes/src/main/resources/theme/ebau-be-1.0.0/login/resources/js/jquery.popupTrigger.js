/*!
 * @class  PopupTrigger
 * @classdesc opens popup and calls a callback function when the popup is closed
 * @author Patrick Görsch, Daniel Rey
 */
;
(function (window, document, $, undefined) {
    "use strict";

    $.fn.popupTrigger = function (callback) { var href = $(this).attr("href");
        var popup = window.open(href, 'popup_basket', 'width=640,height=480');
        if (callback && typeof(callback) === 'function') {
            var timer = setInterval(isPopupOpen, 500);
        }

        function isPopupOpen() {
            if (popup.closed) {
                clearInterval(timer);
                callback();
                return false;
            }
            return true;
        }
    };

})(window, document, jQuery);
