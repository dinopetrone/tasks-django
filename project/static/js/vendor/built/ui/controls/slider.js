define(function(require, exports, module){

var _ = require('underscore');
var marionette = require('marionette');
var dragEvents = require('built/core/events/drag');
var composeAll = require('built/core/utils/helpers').composeAll;

var SliderContainer = marionette.Controller.extend({

    _driver: null,
    _uiUpdater: null,

    /**
     * Initialize slider container
     * @param  {options} options options literal
     * @return {undefined}
     *
     * @example
     * var sliderContainer = new SliderContainer({
     *     driver: new HorizontalSliderControl({
     *         // slider options
     *         // see built/core/controls/horizontal.js
     *     })
     * });
     */
    initialize: function(options){
        this.options = _.defaults(options, this._getDefaults());
        this._driver = this._initializeDriver(this.options);
        this._uiUpdater = this._initializeUiUpdater(this._driver.options);
    },

    onClose: function() {
        this._driver.close();
    },

    _getDefaults: function() {
        return {
            driver: null
        };
    },

    _initializeDriver: function(options) {
        var driver = options.driver;

        if(_.isEmpty(driver)) throw 'Undefined driver.';

        this.listenTo(driver, dragEvents.DRAG_UPDATE, this._dragDidUpdate);

        driver.$container.css({
            position: 'relative'
        });

        driver.$track.css({
            position: 'relative'
        });

        driver.$handles.css({
            position: 'absolute',
            top: '0',
            left: '0'
        });

        return driver;
    },

    _initializeUiUpdater: function(options) {
        return options.snap ? this._updateUiWithSnap : this._updateUi;
    },

    _updateUi: function($handle, range, position, value) {
        $handle.css({'left': value + 'px'});
    },

    _updateUiWithSnap: function($handle, range, position, value) {
        var step, stepDelta;

        step = this._driver.getStepForHandle($handle);
        stepDelta = range.getMax() / this._driver.options.steps;

        // augment position and value
        value = stepDelta * step;

        // pass in augmented values to original update function
        this._updateUi($handle, range, position, value);
    },

    _dragDidUpdate: function(sender, $handle, range, position, value) {
        this._uiUpdater($handle, range, position, value);

        this._driver._dispatchDragUpdate.apply(this, arguments);
    }

}); // eof SliderContainer

// Exports
module.exports.SliderContainer = SliderContainer;

}); // eof define
