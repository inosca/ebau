/*
 KTBE Mobile, Release 4.3
 Letzte Änderung 22.7.2015 (fmel)
 */

/* global Anzeixer, MobileDetect, getCookie, isNotEmpty */

/**
 * Main module for Kanton Bern
 *
 * @copyright 2014 Zeix AG
 */
var ktbe = (function ($) {
    'use strict';

    // public, will be returned
    var my = {};

    //jquery objects
    var $body = $('body');
    var $lightBox = $('.lb');

    $(document).ready(function () {

        my.md = new MobileDetect(window.navigator.userAgent);
        my.lang = $('html').attr('lang');

        my.localizedStrings = {
            showNav: {
                'de': 'Navigation einblenden',
                'fr': 'Afficher la navigation',
                'en': 'Show Navigation'
            },
            hideNav: {
                'de': 'Navigation ausblenden',
                'fr': 'Cacher la navigation',
                'en': 'Hide Navigation'
            },
            switchToDesktop: {
                'de': 'Zur klassischen Ansicht wechseln',
                'fr': 'Affichage classique',
                'en': 'Switch to classic view'
            },
            switchToMobile: {
                'de': 'Zur mobilen Ansicht wechseln',
                'fr': 'Affichage mobile',
                'en': 'Switch to mobile view'
            },
            closeImageLightbox: {
                'de': 'Schliessen',
                'fr': 'Fermer',
                'en': 'Close'
            }
        };


        // not reliable for IE11, see below
        function getIEVersion() {
            var rv = -1;
            if (navigator.appName === 'Microsoft Internet Explorer') {
                var ua = navigator.userAgent;
                var re = new RegExp('MSIE ([0-9]{1,}[.0-9]{0,})');
                if (re.exec(ua) !== null) {
                    rv = parseFloat(RegExp.$1);
                }
            }
            return rv;
        }


        function getExplorerVersion() {
            var sAgent = window.navigator.userAgent;
            var Idx = sAgent.indexOf('MSIE');

            // If IE, return version number.
            if (Idx > 0) {
                return parseInt(sAgent.substring(Idx + 5, sAgent.indexOf('.', Idx)));

                // If IE 11 then look for Updated user agent string.
            } else if (!!navigator.userAgent.match(/Trident\/7\./)) {
                return 11;

                //It is not IE
            } else {
                return 0;
            }
        }


        // android default browser + dolphin = not gecko
        // used for a few icon background sprite adjustments
        var FF = (window.mozInnerScreenX !== null);
        if (FF) {
            $('body').addClass('gecko');
        }

        // detect FF
        var isFirefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;
        if (isFirefox) {
            $body.addClass('firefox');
        }


        var version = getIEVersion();

        if (getExplorerVersion() > 0) {
            $body.addClass('msie');
        }

        if (version <= 9 && version > -1) {
            $body.addClass('ie9orOlder');
        }

        if ($body.hasClass('author')) {
            $.cookie('ktbe_preference_fontsize_mobile', null, {path: '/'});
            $.cookie('ktbe_preference_display_version', null, {path: '/'});
        }

        if ($.cookie('ktbe_preference_fontsize_mobile') === 'big') {
            $body.addClass('bigFont');
        }

        if ($.cookie('ktbe_preference_display_version') === 'desktop') {

            $('#responsive-styles').prop('disabled', true); // disable responsive.css - new method
            $('#responsive-scripts').remove(); // remove responsive.js
            $body.addClass('classic');
            $('.switch-to-desktop').html(my.localizedStrings.switchToMobile[my.lang]);
        }


        // no cookie set + desktop: hide switch link completely
        if (!$.cookie('ktbe_preference_display_version') && Anzeixer.isDesktop()) {
            $('#footer-classic-view').css('display', 'none');
        }


        if (!my.md.mobile()) {
            $('#footer-classic-view').css('display', 'none');
        }


        if ($('#datepicker').length || $('.news-archive').length) {
            // hide jQuery datepicker on mobile, use native date widget
            //  if ( my.md.mobile() || getIEVersion() < -1 ) {
            if (my.md.mobile()) {
                $('#datepicker, #datepicker-von, #datepicker-bis').attr('type', 'date');
                $('.ui-datepicker-trigger').css('display', 'none');
            }
        }


        // user choices:
        // -------------------------
        // preferred font-size: regular or big

        // hide mobile user-choices altogether for desktop users:
        if (!my.md.mobile()) {
            $('#footer-resize-text').css('display', 'none');
            $('.switch-to-desktop').css('display', 'none');
        }

        $('#footer-resize-text').click(function () {

            if (!my.md.mobile()) {
                return;
            }

            // new version: set body class .bigFont
            if (!$body.hasClass('bigFont')) {
                $body.addClass('bigFont');
                $.cookie('ktbe_preference_fontsize_mobile', 'big', {
                    expires: 30,
                    path: '/'
                });
            } else {
                $body.removeClass('bigFont');
                $.cookie('ktbe_preference_fontsize_mobile', 'default', {
                    expires: 30,
                    path: '/'
                });
            }

            ktbe.menu.hideMenu();
            ktbe.menu.placeMenuTrigger();

        });

        // mobile-only search result sort options (publications)
        $('.search-filter-dropdown').on('change', function (e) {
            window.location = e.target.options[e.target.selectedIndex].value;
        });

        // preferred view: responsive or desktop - for mobile users only
        $('.switch-to-desktop').on('click', function (e) {
            e.preventDefault();

            if (!my.md.mobile()) {
                return;
            }

            // mobile -> classic
            if (($.cookie('ktbe_preference_display_version') === undefined) || ($.cookie('ktbe_preference_display_version') === 'mobile')) {
                $('#wrapper').removeAttr('style');
                $('#responsive-styles').prop('disabled', true);
                $('#responsive-scripts').remove();
                $.cookie('ktbe_preference_display_version', 'desktop', {
                    expires: 30,
                    path: '/'
                });
                $body.addClass('classic');
                $('.switch-to-desktop').html(my.localizedStrings.switchToMobile[my.lang]);

                // classic -> mobile
            } else {
                if ($.cookie('ktbe_preference_display_version') === 'desktop') {
                    $('#responsive-styles').prop('disabled', false); // new
                    //$body.append('<script type="text/javascript" src="/js/responsive.js" id="responsive-scripts"></script>');
                    $body.append('<script type="text/javascript" src="/etc/designs/std/js/bottom/responsive.js" id="responsive-scripts"></script>');
                    $body.removeClass('classic');
                    $.cookie('ktbe_preference_display_version', 'mobile', {
                        expires: 30,
                        path: '/'
                    });
                    $('.switch-to-desktop').html(my.localizedStrings.switchToDesktop[my.lang]);
                }
            }
            location.reload();
        });

        // Tabs on Search Page Handling.
        $('.searchresults .tabs li a').on('click', function () {
            var $container = $(this).closest('.searchresults'),
                id = $(this).closest('li').attr('id');
            $container.find('li.active').removeClass('active');
            $container.find('#' + id).addClass('active');
            $container.find('div#pages').css('visibility', 'hidden');
            $container.find('div#pages').css('display', 'none');
            $container.find('div#doc').css('visibility', 'hidden');
            $container.find('div#doc').css('display', 'none');
            $container.find('div#mm').css('visibility', 'hidden');
            $container.find('div#mm').css('display', 'none');
            $container.find('div#others').css('visibility', 'hidden');
            $container.find('div#others').css('display', 'none');

            $('.searchresults .accordion-tab').removeClass('active');
            $('#accordion-' + id).addClass('active');

            var activeDiv = 'pages';

            switch (id) {
                case 'tab-1':
                    activeDiv = 'pages';
                    break;
                case 'tab-2':
                    activeDiv = 'doc';
                    break;
                case 'tab-3':
                    activeDiv = 'mm';
                    break;
                case 'tab-4':
                    activeDiv = 'others';
                    break;
                default:
                    activeDiv = 'pages';
            }
            var activeElement = $('#' + activeDiv);
            if (activeElement) {
                activeElement.css('visibility', 'visible');
                activeElement.css('display', 'block');
            }
        });

        // Accordion on Search Page Handling.
        $('.searchresults .accordion-tab').on('click', function (e) {
            e.preventDefault();
            var $container = $(this).closest('.searchresults'),
                $content = $(this).next('.search-results'),
                id = $content.attr('aria-labelledby');
            var activeDiv = 'pages';

            switch (id) {
                case 'tab-1':
                    activeDiv = 'pages';
                    break;
                case 'tab-2':
                    activeDiv = 'doc';
                    break;
                case 'tab-3':
                    activeDiv = 'mm';
                    break;
                case 'tab-4':
                    activeDiv = 'others';
                    break;
                default:
                    activeDiv = 'pages';
            }

            var activeElement = $('#' + activeDiv);
            if ($content) {
                if ($content.css('visibility') === 'hidden') {
                    $container.find('.search-results').css('visibility', 'hidden');
                    $container.find('.search-results').css('display', 'none');
                    $container.find('.accordion-tab').removeClass('active');


                    $content.css('visibility', 'visible');
                    $content.css('display', 'block');

                    $(this).addClass('active');
                } else {
                    activeElement.css('visibility', 'hidden');
                    activeElement.css('display', 'none');

                    $(this).removeClass('active');
                }
            }

            $('.searchresults .tabs li').removeClass('active');
            $('#' + id).addClass('active');

        });

        // image lightbox stuff:
        var activityIndicatorOn = function () {
            $('<div id="imagelightbox-loading"><div></div></div>').appendTo('body');
        };

        var activityIndicatorOff = function () {
            $('#imagelightbox-loading').remove();
        };

        var overlayOn = function () {
            $('<div id="imagelightbox-overlay"></div>').appendTo('body');
        };

        var overlayOff = function () {
            $('#imagelightbox-overlay').remove();
        };

        var closeButtonOn = function (instance) {
            $('<a href="#" id="imagelightbox-close">' + my.localizedStrings.closeImageLightbox[my.lang] + '</a>').appendTo('body').on('click touchend', function (e) {
                e.preventDefault();
                $(this).remove();
                instance.quitImageLightbox();
            });
        };

        var closeButtonOff = function () {
            $('#imagelightbox-close').remove();
        };

        var captionOn = function () {
            var description = $('a[href="' + $('#imagelightbox').attr('src') + '"] img').attr('alt');
            if (description.length > 0) {
                $('<div id="imagelightbox-caption">' + description + '</div>').appendTo('body');
            }
        };

        var captionOff = function () {
            $('#imagelightbox-caption').remove();
        };

        var navigationOn = function (instance, selector) {
            var images = $(selector);
            if (images.length) {
                var nav = $('<div id="imagelightbox-nav"></div>');
                for (var i = 0; i < images.length; i++) {
                    nav.append('<a href="#"></a>');
                }

                nav.appendTo('body');
                nav.on('click touchend', function () {
                    return false;
                });

                var navItems = nav.find('a');
                navItems.on('click touchend', function () {
                    var $this = $(this);
                    if (images.eq($this.index()).attr('href') !== $('#imagelightbox').attr('src')) {
                        instance.switchImageLightbox($this.index());
                    }

                    navItems.removeClass('active');
                    navItems.eq($this.index()).addClass('active');

                    return false;
                }).on('touchend', function () {
                    return false;
                });
            }
        };

        var navigationUpdate = function (selector) {
            var items = $('#imagelightbox-nav a');
            items.removeClass('active');
            items.eq($(selector).filter('[href="' + $('#imagelightbox').attr('src') + '"]').index(selector)).addClass('active');
        };

        var navigationOff = function () {
            $('#imagelightbox-nav').remove();
        };


        if (!$body.hasClass('author')) {
            $('a.lightbox').imageLightbox({
                //selector:       'id="imagelightbox"',   // string;
                allowedTypes: 'png|jpg|jpeg|gif', // string;
                animationSpeed: 250, // integer;
                preloadNext: false, // bool;            silently preload the next image
                enableKeyboard: true, // bool;            enable keyboard shortcuts (arrows Left/Right and Esc)
                quitOnEnd: false, // bool;            quit after viewing the last image
                quitOnImgClick: true, // bool;            quit when the viewed image is clicked
                quitOnDocClick: true, // bool;            quit when anything but the viewed image is clicked
                onStart: false, // function/bool;   calls function when the lightbox starts
                onLoadStart: function () {
                    overlayOn();
                    activityIndicatorOn();
                },
                onLoadEnd: function () {
                    captionOn();
                    activityIndicatorOff();
                },
                onEnd: function () {
                    captionOff();
                    overlayOff();
                    activityIndicatorOff();
                }
            });
        }


        // init add-to-basket lightbox - disable in author mode
        if ($lightBox.length && !$body.hasClass('author')) {
            $lightBox.fancybox({
                modal: true,
                afterClose: function () {
                    updateBasket();
                }
            });
        }

        var CUGUSERINFOJSON = '.cuguserinfo.json';
        var currentPageUrl = window.location.pathname;
        var userInfoServletUrl;
        if (currentPageUrl.indexOf(".") != -1) {
            userInfoServletUrl = currentPageUrl.split('.')[0] + CUGUSERINFOJSON;
        }
        else {
            // fix for KTBE-6053
            userInfoServletUrl = '/de/index' + CUGUSERINFOJSON;
        }

        function updateCugLogInfo() {
            var logInfo = $('#loginfo');
            var logInfoMobile = $('#loginfo-mobile');

            logInfo.removeClass('visible');
            logInfoMobile.removeClass('visible');

            var ktbernLoginCookie = getCookie('ktbernlogin');
            if (isNotEmpty(ktbernLoginCookie) && (ktbernLoginCookie === '1')) {
                $.getJSON(userInfoServletUrl, function (data) {
                    var firstname = data.firstname;
                    var lastname = data.lastname;
                    if (lastname) {
                        var currentValue = logInfo.find('.logout').text();
                        var newValue = currentValue.replace('[FIRST]', firstname);
                        newValue = newValue.replace('[LAST]', lastname);
                        logInfo.find('.logout').text(newValue);
                    }
                });
                logInfo.addClass('visible');
                logInfoMobile.addClass('visible');
            }
        }

        function updateBasket() {
            var basketTop = $('#basket-top');
            var basketTopMobile = $('#basket-top-mobile');
            var ktbernBasketCookie = getCookie('ktbernbasket');

            basketTop.removeClass('visible');
            basketTopMobile.removeClass('visible');

            if (isNotEmpty(ktbernBasketCookie) && (ktbernBasketCookie === '1')) {
                $.getJSON(userInfoServletUrl, function (data) {
                    var basketItemCount = data.basketItemCount;
                    if (basketItemCount) {
                        if (basketItemCount > 0) {
                            basketTop.addClass('visible');
                            basketTopMobile.addClass('visible');
                        }
                        basketTop.find('span.info .varBasketItemCount').each(function () {
                            $(this).text(basketItemCount);
                        });
                        basketTopMobile.find('span.info .varBasketItemCount').each(function () {
                            $(this).text(basketItemCount);
                        });
                    }
                });
            }
        }

        updateBasket();
        updateCugLogInfo();

        var mobileReady = $('#mobile-indicator').attr('content');
        if (mobileReady === 'no') {
            $body.removeClass('classic');
            $body.addClass('never-mobile');
            $('#responsive-styles').remove(); // remove responsive.css
            $('#responsive-scripts').remove(); // remove responsive.js
            $('#viewport').prop('content', 'width=device-width, maximum-scale=4.0'); // enable zooming -> KTBE-5813
        }

        if (Anzeixer.isDesktop() || $.cookie('ktbe_preference_display_version') === 'desktop' || mobileReady === 'no') {
            $('#viewport').prop('content', 'width=device-width, maximum-scale=4.0');
            //$('#viewport').prop('content', 'width=device-width, minimum-scale=1.0, maximum-scale=4.0');
        } else {
            $('#viewport').prop('content', 'width=device-width, maximum-scale=1.0');
        }

        $(document).on('click', '.inpopup', function (event) {
            event.preventDefault();
            event.stopPropagation();
            $(this).popupTrigger(updateBasket);
        });


        $(window).on('resize', function () {
            var mobileReady = $('#mobile-indicator').attr('content');
            if (Anzeixer.isDesktop() || $.cookie('ktbe_preference_display_version') === 'desktop' || mobileReady === 'no') {
                //$('#viewport').prop('content', 'width=device-width, minimum-scale=1.0, maximum-scale=4.0');
                $('#viewport').prop('content', 'width=device-width, maximum-scale=4.0');
            } else {
                $('#viewport').prop('content', 'width=device-width, maximum-scale=1.0');
            }

        });

        $('input[type="submit"]').click(function (event) {
            //event.preventDefault();
            updateBasket();
            updateCugLogInfo();
        });


        $('.toggle-basic-password-login').on('click', function (e) {
          $('.kc-basic-password-login').toggle();
        })
    });


    // KAIO (fmel) 22.07.2015
    /* change the link format of phone links in content */ //KTBE-6345

    $(document).ready(function() {

        // tel richtig stellen
        $( "#content" ).find('a[href*="tel://+"]').each(function(){
            $(this).attr('href',$(this).attr('href').replace('tel://+','tel:+'));
        });

        // dem http://+ link die richtige klasse geben
        $("a.extern[href*='http://+']").addClass("phone-number");
        $("a.extern[href*='http://+']").removeAttr("target");
        $("a.extern[href*='http://+']").removeClass("extern");

        // http://+ richtig stellen
        $( "#content" ).find('a[href*="http://+"]').each(function(){
            $(this).attr('href',$(this).attr('href').replace('http://+','tel:+'));
        });

    });


    return my;
}(jQuery));

