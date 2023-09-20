/*!
 * @class  Toc
 * @classdesc Creates a table of content based on headers (h1..h6)
 * @author Oriol Torrent Florensa OrT, Unic AG
 *
 * Edited by Oriol Torrent Florensa, Unic AG - 06.06.2014
 * Edited by Oriol Torrent Florensa, Unic AG - 07.09.2014
 */
;(function(window, document, $, undefined) {
    "use strict";

    // Create the defaults once
    var pluginName = "toc",
        defaults = {
            // Class(es) that Will be appended to the <nav /> element which is wrapping the list of the TOC
            navClass: 'content-nav-anchor',
            // Array of class(es) that can be placed in one or several elements wrapping headers that are meant to remove such headers from the TOC
            ignoredSelectors: ['.toc-ignore'],
            // CQ Wrapper element where the TOC plugin has to start finding DIV element until another TOC is found
            siblingsReferenceSelector: '.ankerNavigationNeu',
            // String of selectors
            headersSelector: 'h2'// By default, we will include h2 elements in the TOC
        },
        $document = $(document),
        tocCounter = 0;
    pluginName = pluginName.toLowerCase();

    /**
     * Represents a table of content
     * This is the actual plugin constructor
     * @param {object} element - The DOM element to bind the module.
     * @param {object} options - Options overwriting the defaults.
     * @constructor
     */
    function Toc(element, options) {
        var meta;
        this.$element = $(element);

        // Grab plugin options provided via data properties in the html element. Ex:
        // <div class="toc js-toc" data-toc="init" data-toc-options="{'optionA':'someCoolOptionString'}">
        meta = this.$element.data(pluginName+'-options');

        // merge the options coming from:
        // - defaults (defined at the top of this plugin)
        // - options  (defined at the initialization of this plugin, at the very bottom of this file)
        // - meta     (defined at every html element via data-toc-options parameter)
        this.options = $.extend({}, defaults, options, meta);

        // Keep a reference to the wrapper object in the element
        this.$element.data('plugin_'+pluginName, this);

        this.init();
    }

    Toc.prototype = {
        /**
         * Initialize module, bind events
         * @method
         * @public
         */
        init: function() {
            var tocNav = '<nav role="navigation" class="' + this.options.navClass + '">',
                currentHeadingLevel = 0,
                previousHeadingLevel = 0,
                filterOutString = '',
                headersArray = this.options.headersSelector.split(',');

            filterOutString = this._getFilterOutString(this.options.ignoredSelectors, headersArray);

            this.tocElements = this.$element
                .closest(this.options.siblingsReferenceSelector) // Search up the DOM to find the wrapper element from CQ
                .nextUntil(this.options.siblingsReferenceSelector, 'div') // Select only div elements until anoter TOC
                .find(this.options.headersSelector) // Find any header inside
                .not(filterOutString); // Remove those headers in one of the ignored classes

            this._setIds();

            this.tocElements.each($.proxy(function(index, element){
                var $element = $(element),
                    openlistsLeft = 0;

                // Update params/counters
                previousHeadingLevel = currentHeadingLevel;
                currentHeadingLevel = this._getHeadingLevel($element);

                if (currentHeadingLevel !== false) {
                    if ( currentHeadingLevel > previousHeadingLevel ) {
                        tocNav += '<ul><li>';
                    }
                    if ( currentHeadingLevel < previousHeadingLevel ) {
                        tocNav += '</li></ul><li>';
                    }
                    if ( currentHeadingLevel === previousHeadingLevel ) {
                        tocNav += '</li><li>';
                    }
                    tocNav += '<a href="#'+$element.attr('id')+'">'+$element.text()+'</a>';
                }

                // This is the last loop, so we need to close lists
                if ( this.tocElements.length === index+1 ) {
                    openlistsLeft = previousHeadingLevel - currentHeadingLevel
                    do {
                        tocNav += '</li></ul>';
                        --openlistsLeft;
                    } while (openlistsLeft >= 0);
                }
            }, this));

            tocNav += '</ul></nav>';

            this.$element.append(tocNav);
        },

        /**
         * Build the string of CSS selectors that will be used to filter out headers
         * This is a convination of ignored classes and headers
         * @param  {Array} ignoreSelectors [Array of css class selectors]
         * @param  {Array} headers         [Array of css headers selectors]
         * @return {String}                [Coma separated string of CSS selecors]
         */
        _getFilterOutString: function(ignoreSelectors, headers) {
            var filterOutString = '';
            $.each(ignoreSelectors, function(i, ignoredSelector) {
                $.each(headers, function(j, header) {
                    filterOutString += $.trim(ignoredSelector) + ' ' + $.trim(header) + ', ';
                });
            });
            return $.trim(filterOutString).slice(0, -1); // Remove ', ' from the end of the string
        },

        /**
         * Adds an id to every element from the TOC
         * @private
         */
        _setIds: function() {
            this.tocElements.each(function(index, element) {
                var $element = $(element);
                if ( typeof($element.attr('id')) === 'undefined' ) {
                    ++tocCounter;
                    $element.attr('id', 'anker-anchor-'+tocCounter);
                }
            });
        },

        /**
         * Parse the received heading element and returns its level
         * @param  {object} $element [the heading element passed as a jQuery object]
         * @return {number}          [numeric level from the passed heading element]
         * @private
         */
        _getHeadingLevel: function($element) {
            var level;
            if (
                $element.prop('tagName').toLowerCase() === 'h1' ||
                $element.prop('tagName').toLowerCase() === 'h2' ||
                $element.prop('tagName').toLowerCase() === 'h3' ||
                $element.prop('tagName').toLowerCase() === 'h4' ||
                $element.prop('tagName').toLowerCase() === 'h5' ||
                $element.prop('tagName').toLowerCase() === 'h6'
                ) {
                level = parseInt($element.prop('tagName').substring(1));
            } else {
                level = false;
            }
            return level;
        },

        /**
         * Remove the plugin without removing the DOM element
         * @method
         * @example
         * Usage from inside this plugin:
         * this.destroy();
         * Usage from outside a plugin:
         * jQuery('[data-toc=init]').toc('destroy');
         * @public
         */
        destroy: function() {
            this.$element.off('.' + pluginName);
            // this.$element.find('*').off('.' + pluginName);
            this.$element.removeData( 'plugin_' + pluginName );
            this.$element.removeData( pluginName );
            this.$element.find('.'+this.options.navClass).remove();
        },

        /**
         * Wrapper method to destroy and init again
         * @param  {object} event [jQuery object that wraps the custom event]
         * @return {[type]}       [description]
         * @public
         */
        reInit: function(event) {
            if(typeof event !== 'undefined') {
                if(preventDefault in event && typeof event.preventDefault !== 'undefined') {
                    event.preventDefault();
                    event.stopPropagation();
                }
            }
            this.destroy();
            this.init();
        }
    };


    /**
     * A lightweight plugin wrapper around the constructor,
     * preventing against multiple instantiations and allowing any
     * public function (ie. a function whose name doesn't start
     * with an underscore) to be called via the jQuery plugin,
     * e.g. $(element).toc('functionName', arg1, arg2)
     *
     * @param {object} options [description: options passed on plugin initialization]
     */
    $.fn[pluginName] = function(options) {
        var args = arguments;
        if (options === undefined || typeof options === 'object') {
            return this.each(function() {
                if (!$.data(this, 'plugin_' + pluginName)) {
                    // $.data(this, 'plugin_' + pluginName, new Toc(this, options));
                    new Toc(this, options);
                }
            });
        } else if (typeof options === 'string' && options[0] !== '_' && options !== 'init') {
            return this.each(function() {
                var instance = $.data(this, 'plugin_' + pluginName);
                if (instance instanceof Toc && typeof instance[options] === 'function') {
                    instance[options].apply(instance, Array.prototype.slice.call(args, 1));
                }
            });
        } else {
            throw 'Illegal usage of the plugin: ' + pluginName;
        }
    };

    // Bind the module on particular events and elements
    $document.on('ready ajax_loaded', function() {
        $.fn[pluginName].apply($('[data-'+ pluginName +'~=init]'), [{}]);
    });

    $document.on('DOMNodeInserted', '[data-'+ pluginName +'~=init]', function(event) {
        if ( $(event.target).attr('data-'+ pluginName) === 'init' ) {
            $.fn[pluginName].apply($(event.target), [{}]);
            $('[data-'+ pluginName +'~=init]').toc('reInit', event);
        }
        event.preventDefault();
        event.stopPropagation();
    });

})(window, document, jQuery);
