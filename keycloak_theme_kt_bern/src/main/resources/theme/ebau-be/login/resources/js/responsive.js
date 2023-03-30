/*
KTBE Mobile, Release 4.3
Letzte Änderung 22.7.2015 (fmel)
*/

/* global Anzeixer, ktbe */

/**** Start always on top ****/
// BeforUnLoad: Ensure that viewport is on top
$(window).on('beforeunload', function() {
  'use strict';
  if (!Anzeixer.isDesktop() && !window.location.hash) {
    $(window).scrollTop(0);
  }
});




/**** Set classes to collapsible h1 titles on start page ****/
$(document).ready(function() {
  $('#content-col-nav h1.collapsible').first().addClass('first');
  $('#content-col-main h1.collapsible').first().addClass('first');
  $('#content-col-context h1.collapsible').first().addClass('first');
});




/**** Set margin of Content according to height of Header ****/
ktbe.setMarginTop = function() {

  'use strict';

  if (!$('body').hasClass('portal')) {
    var marginTop = $('#div_header').outerHeight(true) + 20;

    // If: only on start page of directions; else: any other page
    if (!$('body').hasClass('classic') && !Anzeixer.isDesktop()) {

      if ($('body#home #content-col-nav').length !== 0) {

        $('#content-col-nav').css('margin-top', marginTop);

        $('#content-col-main').css('margin-top', '0');

      } else {

        $('#content-col-main').css('margin-top', marginTop);

      }

    } else if (!$('body').hasClass('classic') && Anzeixer.isDesktop()) {
        if ($('body').attr('id') === 'home') {

          $('#content-col-nav').css('margin-top', '33px');

          $('#content-col-main').css('margin-top', '33px');

        } else {

          $('#content-col-nav').css('margin-top', 'auto');

          $('#content-col-main').css('margin-top', 'auto');

        }

    } else if ($('body').hasClass('classic')) {

        $('#wrapper').removeAttr('style');

        if ($('body').attr('id') === 'home') {

          $('#content-col-nav').css('margin-top', '33px');

          $('#content-col-main').css('margin-top', '33px');

        } else {

          $('#content-col-nav').css('margin-top', 'auto');

          $('#content-col-main').css('margin-top', 'auto');

        }

    }
  }
};

$(document).on('ready', function() {
    'use strict';
    ktbe.setMarginTop();
});
$(window).on('resize', function() {
    'use strict';
    ktbe.setMarginTop();
});





/**** NAVIGATION MENU ****/
ktbe.menu = (function($) {

  'use strict';
  var my = {};

  /** Variables **/
  /* Viewport */
  var viewportWidth = $(window).width();
  var viewportHeight;
  var viewportMenuUpperBound; // menu fills maximum this portion of the viewport (default setting; equals start point of initial menu animation; is ignored in special cases)
  var viewportMenuLowerBound; // at the end of initial menu animation is maxium this portion visible in the viewport (default setting; is ignored in special cases)

  /* Navigation related elements and properties */
  var $showContentArea;
  var $showContentButton;
  var $hauptNavigationMobile;
  var $footer;
  var $wrapper;

  var showContentAreaHeight;
  var hauptNavigationMobileHeight;
  var menuTotalHeight;
  var footerHeight;

  /* Position Values */
  var scrollPosition;
  var menuStartPosition;
  var menuListStartPosition;
  var menuEndPosition;
  var menuListEndPosition;
  var wrapperStartHeight;
  var wrapperEndHeight;
  var menuDefaultHiddenPosition;
  var menuListDefaultHiddenPositon;
  var wrapperDefaultHiddenPosition;
  var footerDefaultPosition;

  /* Time Values */
  var animationTimeMenu = 400;

  $showContentArea = $('#show-content-area');
  $showContentButton = $('.show-content');
  $hauptNavigationMobile = $('#hauptNavigation-mobile');
  $footer = $('#footer');
  $wrapper = $('#wrapper');


  /** Basic functions **/
  /* Calculation of basic values */
  var calculateBasicValues = function() {

    viewportHeight = $(window).height();
    viewportMenuUpperBound = viewportHeight * 2 / 3; // menu fills maximum this portion of the viewport (default setting; equals start point of initial menu animation; is ignored in special cases)
    viewportMenuLowerBound = viewportHeight / 3; // at the end of initial menu animation is maxium this portion visible in the viewport (default setting; is ignored in special cases)

    $hauptNavigationMobile.show();
    $('#navigation-background').show();

    hauptNavigationMobileHeight = $('#navigation-background').outerHeight(true);
    showContentAreaHeight = $showContentButton.outerHeight(true);
    $showContentArea.css('height', showContentAreaHeight);
    menuTotalHeight = showContentAreaHeight + hauptNavigationMobileHeight;
    footerHeight = $footer.outerHeight(true);

  };

  /* Calculation of position values */
  var calculateMenuPositionValues = function() {

    if (!Anzeixer.isDesktop()) {

      scrollPosition = window.pageYOffset;

      // If: $footer is in viewport; else: $footer is not in viewport
      if (window.pageYOffset + viewportHeight > $footer.offset().top) {

        // If: menu exeeds maximum height in viewport; else: menu does not exeed maxium height in viewport
        if (menuTotalHeight > viewportMenuUpperBound) {

            menuStartPosition = $footer.offset().top;
            menuEndPosition = menuStartPosition;
            wrapperStartHeight = $footer.offset().top + viewportHeight + footerHeight;
            wrapperEndHeight = wrapperStartHeight;

        } else {

            menuStartPosition = viewportHeight - menuTotalHeight + scrollPosition;
            wrapperStartHeight = viewportHeight + scrollPosition;

            if (menuTotalHeight >= viewportMenuLowerBound) {

              menuEndPosition = viewportMenuUpperBound + scrollPosition;
              wrapperEndHeight = viewportMenuUpperBound + menuTotalHeight + scrollPosition;

            } else {

              menuEndPosition = menuStartPosition;
              wrapperEndHeight = wrapperStartHeight;

            }

        }

      } else {

          // If: menu exeeds maximum height in viewport; else: menu does not exeed maxium height in viewport

          if (menuTotalHeight > viewportMenuUpperBound) {

            menuStartPosition = viewportMenuLowerBound + scrollPosition;
            menuEndPosition = viewportMenuUpperBound + scrollPosition;
            wrapperStartHeight = viewportMenuLowerBound + menuTotalHeight + scrollPosition;
            wrapperEndHeight = viewportMenuUpperBound + menuTotalHeight + scrollPosition;

          } else {

            menuStartPosition = viewportHeight - menuTotalHeight + scrollPosition;
            wrapperStartHeight = viewportHeight + scrollPosition;

            if (menuTotalHeight >= viewportMenuLowerBound) {

              menuEndPosition = viewportMenuUpperBound + scrollPosition;
              wrapperEndHeight = viewportMenuUpperBound + menuTotalHeight + scrollPosition;

            } else {

              menuEndPosition = menuStartPosition;
              wrapperEndHeight = wrapperStartHeight;

            }

          }

      }

      menuListStartPosition = menuStartPosition + showContentAreaHeight;
      menuListEndPosition = menuEndPosition + showContentAreaHeight;

      menuDefaultHiddenPosition = scrollPosition + viewportHeight - showContentAreaHeight;
      menuListDefaultHiddenPositon = scrollPosition + viewportHeight;
      wrapperDefaultHiddenPosition = scrollPosition + viewportHeight + hauptNavigationMobileHeight;

    }

  };

  /* Start the default animation / presentation of the menu */
  var startInitialMenuAnimation = function() {

    if (!Anzeixer.isDesktop() && !$('body').hasClass('menu-hidden')) {

      // If: $footer is in viewport; else: footer is not in viewport
      if (window.pageYOffset + viewportHeight >= $footer.offset().top) {

          // special case: other position values than calculated by the function calculateMenuPositionValues()
          menuEndPosition = viewportMenuUpperBound;
          menuStartPosition = menuEndPosition;
          wrapperEndHeight = viewportMenuUpperBound + menuTotalHeight;
          wrapperStartHeight = wrapperEndHeight;
          menuListEndPosition = menuEndPosition + showContentAreaHeight;
          menuListStartPosition = menuListEndPosition;

      } else {

          calculateMenuPositionValues();

      }
      $showContentArea.css({
          'display': 'block',
          'position': 'absolute',
          'top': menuStartPosition,
          'right': '0'
      });
      $hauptNavigationMobile.css({
          'display': 'block',
          'position': 'absolute',
          'top': menuListStartPosition
      });
      $wrapper.css({
          'height': wrapperStartHeight
      });

      if (menuTotalHeight > viewportMenuLowerBound) {



          $showContentArea.animate({

            top: menuEndPosition

          }, animationTimeMenu);

          $hauptNavigationMobile.animate({

            top: menuListEndPosition

          }, animationTimeMenu);

          $wrapper.animate({

            height: wrapperEndHeight

          }, animationTimeMenu);

      }

    }

  };


  /* Show menu on demand (menu will move upwards from top of the footer when menu button is locked to the $footer (first if-statement) or from the bottom of the viewport) */
  my.showMenu = function() {

    if (!Anzeixer.isDesktop()) {
      calculateBasicValues();
      footerDefaultPosition = $footer.offset().top;

      // If: $footer is in viewport; else: $footer is not in viewport
      if (window.pageYOffset + viewportHeight >= footerDefaultPosition) {

        // When $footer is in viewport at the beginning, then make own position calculations (not using the function calculateMenuPositonValues() )
        menuStartPosition = footerDefaultPosition - showContentAreaHeight;
        menuEndPosition = footerDefaultPosition - menuTotalHeight;
        wrapperStartHeight = footerDefaultPosition;
        wrapperEndHeight = wrapperStartHeight;
        menuListStartPosition = footerDefaultPosition;
        menuListEndPosition = footerDefaultPosition + showContentAreaHeight - menuTotalHeight;

        var scrollTarget = footerDefaultPosition - menuTotalHeight - viewportMenuLowerBound;

        $hauptNavigationMobile.show();
        $showContentArea.css({
            'top': menuStartPosition,
            'position': 'absolute'
        });
        $showContentButton.css({
            'position': 'relative'
        });
        $hauptNavigationMobile.css('top', menuListStartPosition);
        $footer.css({
            'position': 'absolute'
        });
        $wrapper.css({
            'height': wrapperStartHeight
        });

        $('body').removeClass('menu-hidden');
        $showContentButton.text(ktbe.localizedStrings.hideNav[ktbe.lang]);
        $showContentArea.animate({
            top: menuEndPosition
        }, animationTimeMenu);

        $hauptNavigationMobile.animate({
            top: menuListEndPosition
        }, animationTimeMenu);

        $wrapper.animate({
            height: wrapperEndHeight
        }, animationTimeMenu);

        $('html, body').animate({
            scrollTop: scrollTarget
        }, animationTimeMenu);

      } else {

        $hauptNavigationMobile.show();
        calculateMenuPositionValues();
        $showContentArea.css({
            'top': menuDefaultHiddenPosition,
            'position': 'absolute',
            'bottom': 'auto'
        });
        $showContentButton.css({
            'position': 'relative'
        });
        $hauptNavigationMobile.css('top', menuListDefaultHiddenPositon);
        $wrapper.css('height', wrapperDefaultHiddenPosition);

        $('body').removeClass('menu-hidden');
        $showContentButton.text(ktbe.localizedStrings.hideNav[ktbe.lang]);
        $showContentArea.animate({
            top: menuStartPosition
        }, animationTimeMenu);

        $hauptNavigationMobile.animate({
            top: menuListStartPosition
        }, animationTimeMenu);

        $wrapper.animate({
            height: wrapperStartHeight
        }, animationTimeMenu);

      }

    }

  };


  /* Hide menu on demand */
  my.hideMenu = function() {

    if (!Anzeixer.isDesktop() && !$('body').hasClass('classic')) {

      $('body').addClass('menu-hidden');
      $showContentButton.text(ktbe.localizedStrings.showNav[ktbe.lang]);
      $wrapper.css('height', 'auto');
      $hauptNavigationMobile.hide();

    }

  };


  /* Lock menu button to the top of the footer or release it */
  my.placeMenuTrigger = function() {

    if (!Anzeixer.isDesktop()) {

      if ($('body').hasClass('menu-hidden')) {
        if (window.pageYOffset + viewportHeight > $footer.offset().top) {
            $showContentArea.css({
                'position': 'absolute',
                'top': $footer.offset().top - showContentAreaHeight
            });
            $showContentButton.css({

            });

        } else {

            $showContentArea.css({
                'position': 'fixed',
                'bottom': '0',
                'top': 'auto'
            });
            $showContentButton.css({
                'bottom': '0'
            });

        }

      } else {

        if (window.pageYOffset + viewportHeight < $showContentArea.offset().top + showContentAreaHeight) {
            my.hideMenu();
        }
      }

    }

  };


  /* Event triggered functions */
  $(document).on('ready', function() {

    // OnDocumentReady: Start the default animation / presentation of the menu
    calculateBasicValues();

    if (window.location.hash) {
      my.hideMenu();
      my.placeMenuTrigger();
    } else {
        startInitialMenuAnimation();
    }
    // OnScroll: Lock menu button to the top of the footer or release it
    $(document).on('scroll touchstart', function() {
      my.placeMenuTrigger();
    });
    // OnClick (Menu button): Toggle navigation menu
    $showContentArea.click(function(event) {

      event.preventDefault();

      if ($('body').hasClass('menu-hidden')) {
        my.showMenu();
      } else {
        my.hideMenu();
        my.placeMenuTrigger();
      }

    });

    // OnClick/Touchstart (Content area): Hide navigation menu
    // IE10/11-Exception
    var eventType;
    if (window.navigator.pointerEnabled) {
      //$('#content, #az, #footer-resize-text').on("pointerdown", function() {
      $('#content, #az').on("pointerdown", function() {
        onPointerDown();
      });

    } else if (window.navigator.msPointerEnabled) {
      //$('#content, #az, #footer-resize-text').on("MSPointerDown", function() {
      $('#content, #az').on("MSPointerDown", function() {
        onPointerDown();
      });
    }
    // Default
    //$('#content, #az, #footer-resize-text').on('click touchstart', function() {
    $('#content, #az').on('click touchstart', function() {
        onPointerDown();
    });

    function onPointerDown() {
      my.hideMenu();
      my.placeMenuTrigger();
    }

    if ($('body').hasClass('classic')) {
      $('#wrapper').removeAttr('style');
    }

  });

  $(window).on('resize', function() {

    var viewportWidthBefore = viewportWidth;
    viewportWidth = $(window).width();

    if (!Anzeixer.isDesktop() && viewportWidthBefore != viewportWidth) {
      calculateBasicValues();
      my.hideMenu();
      my.placeMenuTrigger();
    }
  });

  return my;

}(jQuery));




/**** Expand & Collapse ****/
ktbe.expandAndCollapse = (function($) {

  'use strict';

  var my = {};

  $(document).on('ready', function() {

    // OnDocumentReady: Add classes for collapsed state of accordeon content on home

    $('body#home h1.collapsible').addClass('collapsed');
    $('body#home h1.collapsible').next().addClass('collapsed');

    // OnDocumentReady: Add classes for collapsed state of collapsed contact box
    $('.box .title.collapsible').addClass('collapsed');
    $('.box .body.collapsible').addClass('collapsed');

    // OnClick (Accordeon on home): Expand or collapse

    $('body#home h1.collapsible').click(function() {
      $(this).toggleClass('collapsed');
      $(this).next().toggleClass('collapsed');
    });

    // OnClick (Contact box): Expand or collapse

    $('.box .title.collapsible').click(function() {
      $(this).toggleClass('collapsed');
      $(this).next().toggleClass('collapsed');
    });

  });

  return my;

}(jQuery));




/**** Flyouts (search, a-z) ****/
ktbe.flyoutsShowAndHide = (function($) {

  'use strict';

  var my = {};

  $(document).on('ready', function() {

    // Toggle visibility of search flyout and lightbox
    // disabled due to KTBE-5984
    //$('#toggle-search').click(function() {
    //
    //  $('body').removeClass('az-open');
    //
    //  $('body').toggleClass('search-open');
    //
    //});

    // Toggle visibility of themes a-z flyout and lightbox

    $('#toggle-az, .toggle-az-inpage').click(function() {

      $('body').removeClass('search-open');

      $('body').toggleClass('az-open');

    });

    // Toggle visibility of search or flyout and lightbox when clicked on lightbox or the close-links within the flyouts

    $('#lightbox, #header-search-mobile .schliessen a, #header-nav-meta-mobile #close-az, #header-nav-meta-mobile ul li a').click(function() {

      $('body').removeClass('search-open az-open');

    });

  });

  $(window).resize(function() {
    if(Anzeixer.isDesktop()) {
      $('body').removeClass('az-open search-open');
    }
  });

  return my;

}(jQuery));




/**** Hide & Show Header ****/
ktbe.headerShowAndHide = (function($) {

  'use strict';

  var my = {};

  $(document).on('ready', function() {

    var scrollPos = 0;

    var scrollTime;

    // OnScroll: Show header onScrollUp and hide header onScrollDown

    $(window).scroll(function() {

      clearTimeout(scrollTime);

      var currentScroll = $(window).scrollTop();

      var headerHeight = $('#div_header').outerHeight(true);

      if (currentScroll > scrollPos && window.pageYOffset > headerHeight) {

        $('#div_header').addClass('header-hidden').css('top', -headerHeight);

      } else if (currentScroll <= scrollPos) {

        $('#div_header').removeClass('header-hidden').css('top', 0);

      }

      scrollTime = setTimeout(function() {

        scrollPos = $(window).scrollTop();

      }, 100);

    });

  });


  return my;

}(jQuery));




/**** warenkorb Lightbox ****/
var showWarenkorbLightbox = function() {

  'use strict';

  event.preventDefault();

  $('#lightbox-warenkorb-content').load('popup-basket.html');

  $('#lightbox-warenkorb-content').show();

  $('#lightbox-warenkorb').show();

};

var showWarenkorbPopUp = function() {

  'use strict';

  window.open('popup-basket.html', 'popup_basket', 'width=640,height=480');

  return false;

};

$(document).ready(function() {

  'use strict';

  $(window).resize(function() {

    $('#link-popup').removeAttr('onclick');

    var viewportWidth = $(window).width();

    if (viewportWidth < 1000) {

      $('#link-popup').off('click').on('click', showWarenkorbLightbox);

    } else {

      $('#link-popup').off('click').on('click', showWarenkorbPopUp);

    }

  });

});



$(document).on('click touchstart', '#lightbox-warenkorb', function(e) {
  'use strict';
  e.preventDefault();
  $('#lightbox-warenkorb-content').hide();
  $('#lightbox-warenkorb').hide();
});



/**** Duplicate Teasers on Startpage DIR ****/
// duplicate teasers and put into placeholder (display AFTER news-items):
var teasers = $('#desktop-teasers').html();
$('#responsive-teasers').html(teasers);
$('#responsive-teasers .box.alternative').addClass('responsive');


/* adapt table.basket: move tfoot below tbody */ //KTBE-5901

$(document).ready(function() {
  var tableFoot = $('table.basket tfoot');
  var tableBody = $('table.basket tbody');

  tableFoot.remove();
  tableBody.after(tableFoot);

});

// KAIO FMEL >>>>>>>>>>>>>
// tel script wieder entfernt und in ktbe.js ergänzt, damit es auch bei nicht mobilen sites greift


/*******************************************
 * Scripts for Portal
 ********************************************/

/**** top navigation tabs toggle ****/
/*
ktbe.topNaviagtionTabs = (function($) {
  'use strict';

  $(document).on('ready', function() {

      //
    $(document).on('click touchstart', '#header-shortcuts .box', function() {
      var $headerShortcutsList = $('ul', $(this));

      // check if certain box already open close it
      if ($(this).closest('.box').hasClass('open')) {
        $('#header-shortcuts .box').removeClass('open');
        $('body').removeClass('top-nav-open');
        return false;
      }

      // check for already opened top navigation tabs
      if ($('#header-shortcuts').find('.open').length > 0) {
        $('#header-shortcuts .box').removeClass('open');
      } else {
        // toggle class for body
        $('body').toggleClass('top-nav-open');
      }

      // toggle class for .box
      $(this).toggleClass('open');

    });

    // close menu and lightbox by click aside

    $(document).on('click touchstart', 'body.top-nav-open #lightbox', function() {
      $('#header-shortcuts .box').removeClass('open');
      $('body').removeClass('top-nav-open');
    });

    // cleanUp hidden list if desktop view
    $(document).on('viewchange', function(e) {
      if (Anzeixer.isDesktop()) {
          $('#header-shortcuts .box').removeClass('open');
          $('body').removeClass('top-nav-open');
      }
    });

  });

}(jQuery));
*/



/**** make none javascript version of startseite coverflow for responsive page ****/
ktbe.responsiveCoverflow = (function($) {
  'use strict';

  var $coverflowHtml = $('#contentFlow .flow').clone();

  $.each($coverflowHtml.find('.item'), function() {
    var $title = $(this).children('.caption').children('h3').clone();
    $(this).children('.caption').children('h3').remove();
    $(this).prepend($title);
  });

  $('#events-mobile').html($coverflowHtml);

}(jQuery));