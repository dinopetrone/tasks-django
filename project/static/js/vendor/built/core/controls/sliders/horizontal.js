define(function(require, exports, module){

var _ = require('underscore');
var marionette = require('marionette');
var RangeManager = require('built/core/managers/range').RangeManager;
var MouseResponder = require('built/core/responders/mouse').MouseResponder;
var TouchResponder = require('built/core/responders/touches').TouchResponder;
var dragEvents = require('built/core/events/drag');
var getElementBounds = require('built/ui/helpers/dom').getElementBounds;
var registerElement = require('built/core/utils/helpers').registerElement;
var composeAll = require('built/core/utils/helpers').composeAll;

var HorizontalSliderControl = marionette.Controller.extend({

    _rangeManagers : null,
    _mouseResponders : null,
    _touchResponders : null,
    _handleOffsets : [],

    /**
     * Initialize HorizontalSliderControl
     * @param  {object} options options literal
     * @return {undefined}
     *
     * @example
     * horizontalSliderControl = new HorizontalSliderControl(
     *     {
     *         container    : $('.slider'),           // required, string or jquery
     *         track        : $('.slider .track'),    // required, string or jquery
     *         handles      : $('.slider .handle'),   // required, string or jquery
     *         steps        : 10,                     // default 0
     *         snap         : flase,                  // default false
     *         acceptsMouse : true                    // default true
     *         acceptsTouch : false                   // default false
     *     }
     * );
     */
    initialize: function(options){
        this.options = _.defaults(options, this._getDefaults());

        this.$container = registerElement(this.options.container, true);
        this.$track     = registerElement(this.options.track,     true);
        this.$handles   = registerElement(this.options.handles,   true);

        this._rangeManagers = this._initializeRanges();

        if(this.options.acceptsMouse){
            this._mouseResponders = this._initializeMouse();
        }
        if(this.options.acceptsTouch){
            this._touchResponders = this._initializeTouch();
        }
    },

    onClose: function() {
        var controllers;

        function iterator (controller, i, list) {
            if(controller) controller.close();
        }

        controllers = (this._mouseResponders || [])
            .concat(this._touchResponders || [])
            .concat(this._rangeManagers || []);

        _.each(controllers, iterator, this);
    },

    // Override / extend return value here to add additional options
    _getDefaults: function() {
        return {
            container: null,
            track: null,
            handles: null,
            steps: 0,
            snap: false,
            acceptsMouse: true,
            acceptsTouch: false
        };
    },

    _initializeRanges: function() {
        var $handles, $track;

        function iterator(handle, i, list) {
            var $handle, listener, range;

            $handle = $(handle);
            listener = _.bind(this._rangeDidChange, this, $handle);
            range = new RangeManager({
                min: 0,
                max: this._calculateNormalizedMaxPosition($handle, $track)
            });

            this.listenTo(range, 'change', listener);

            return range;
        }

        $handles = this.$handles;
        $track = this.$track;

        return _.map($handles, iterator, this);
     },

    _initializeMouse: function() {
        var ranges;

        function iterator(el, i, list) {
            return new MouseResponder({
                el: $(el),
                mouseDragged: _.bind(this._handleDidReceiveDrag, this, ranges[i]),
                mouseDown: _.bind(this._handleDidReceiveDragStart, this, ranges[i]),
                mouseUp: _.bind(this._handleDidReceiveDragEnd,  this, ranges[i])
            });
        }

        ranges = this._rangeManagers;

        return _.map(this.$handles, iterator, this);
    },

    _initializeTouch: function() {
        var ranges;

        function iterator(el, i, list) {
            return new TouchResponder({
                el: $(el),
                touchMove : _.bind(this._handleDidReceiveDrag,      this, ranges[i]),
                touchStart: _.bind(this._handleDidReceiveDragStart, this, ranges[i]),
                touchEnd  : _.bind(this._handleDidReceiveDragEnd,  this, ranges[i])
            });
        }

        ranges = this._rangeManagers;

        return _.map(this.$handles, iterator, this);
    },

    _calculateNormalizedMaxPosition: function($handle, $track) {
        var handleBounds, trackBounds;

        handleBounds = getElementBounds($handle);
        trackBounds = getElementBounds($track);

        return Math.abs(trackBounds.width - handleBounds.width);
    },

    _getHandleIndex: function($handle) {
        var $handles, index;

        $handles = this.$handles;
        index = $handles.index($handle);

        if(index < 0) {
            throw 'Could not retrieve handle from the currently set $handles option.';
        }

        return index;
    },

    _getRangeManager: function(index) {
        var outofrange;

        outofrange = index > this._rangeManagers.length - 1;

        if(outofrange) {
            throw 'Index out of range, this._rangeManagers[' + index + '], when length is ' + this._rangeManagers.length + '.';
        }

        return this._rangeManagers[index];
    },

    /**
     * composes methods into the incoming container scope
     * @param  {object} container the container into which we are composing
     * @return {undefined}
     *
     * @note
     * Override this to add additional composable methods
     */
    compose: function(container) {
        composeAll(
            container,
            this,
            'calculateMaxPosition',
            'getPositionAt',
            'getPositions',
            'getPositionForHandle',
            'setPositionAt',
            'setPositionForHandle',
            'getStepAt',
            'getSteps',
            'getStepForHandle',
            'setStepAt',
            'setStepForHandle',
            'getPosition',
            'setPosition',
            'getStep',
            'setStep'
        );
    },

    calculateMaxPosition: function() {
        var $handles, $track, $handle, range, max;

        function iterator(handle, i, $handles) {
            $handle = $(handle);
            range = this._getRangeManager(i);
            max = this._calculateNormalizedMaxPosition($handle, $track);

            range.setMax(max);
        }

        $handles = this.$handles;
        $track = this.$track;

        _.each(this.$handles, iterator, this);
    },

    getPositionAt: function(index) {
        return this._getRangeManager(index).getPosition();
    },

    getPositions: function() {
        function iter(el, i, list) {
            return this.getPositionAt(i);
        }

        return _.map(this._rangeManagers, iter, this);
    },

    getPositionForHandle: function($handle) {
        var index;

        index = this._getHandleIndex($handle);
        return this.getPositionAt(index);
    },

    setPositionAt: function(value, index) {
        index = index || 0; // default to 0
        this._getRangeManager(index).setPosition(value);
    },

    setPositionForHandle: function(value, $handle) {
        var index;

        index = this._getHandleIndex($handle);
        this.setPositionAt(value, index);
    },

    getStepAt: function(index) {
        var position;

        position = this.getPositionAt(index);

        // round will round-up if decimal is greater than .5.
        // round will round-down if decimal is less than .5.
        // this should give good reporting of steps based on position.
        return Math.round(this.options.steps * position);
    },

    getSteps: function() {
        function iterator(el, i, list) {
            return this.getStepAt(i);
        }

        return _.map(this._rangeManagers, iterator, this);
    },

    getStepForHandle: function($handle) {
        var index;

        index = this._getHandleIndex($handle);
        return this.getStepAt(index);
    },

    setStepAt: function(value, index) {
        var posiiton, steps;

        steps = this.options.steps;

        // isNaN check handles 0/0 case
        position = value/steps;
        position = isNaN(position) ? 0 : position;

        this.setPositionAt(position, index);
    },

    setStepForHandle: function(value, $handle) {
        var index;

        index = this._getHandleIndex($handle);
        this.setStepAt(value, index);
    },

    getPosition: function() {
        return this.getPositionAt(0);
    },

    setPosition: function(value) {
        this.setPositionAt(value, 0);
    },

    getStep: function() {
        return this.getStepAt(0);
    },

    setStep: function(value) {
        this.setStepAt(value, 0);
    },

    // Event delegates

    // TODO: Revisit - Method calling a method here.
    _rangeDidChange: function($handle, range, position, value) {
        this._dispatchDragUpdate($handle, range, position, value);
    },

    _handleDidReceiveDrag: function(range, responder, e) {
        var $handle, index, delta, value;

        e.preventDefault();

        $handle = responder.$el;
        index   = this._getHandleIndex($handle);

        // touch returns array, mouse returns single value.
        // we can use some slight-of-hand to get the correct value.
        // if deltaX()[0] is undefined then
        // return the value of deltaX() only.
        delta = responder.deltaX()[0] || responder.deltaX();
        value = delta + this._handleOffsets[index];

        this.setPositionForHandle(range.calculatePositionForValue(value), $handle);
    },

    _handleDidReceiveDragStart: function(range, responder, e) {
        var $handle, index;

        e.preventDefault();

        $handle = responder.$el;
        index = this._getHandleIndex($handle);

        this._handleOffsets[index] = responder.$el.position().left;

        this._dispatchDragStart(
            responder.$el, range, range.getPosition(), range.getValue());
    },

    _handleDidReceiveDragEnd: function(range, responder, e) {
        e.preventDefault();
        this._dispatchDragEnd(
            responder.$el, range, range.getPosition(), range.getValue());
    },

    // Event dispatchers

    _dispatchDragStart: function($handle, range, position, value) {
        this.trigger(dragEvents.DRAG_START, this, $handle, range, position, value);
    },

    _dispatchDragUpdate: function($handle, range, position, value) {
        this.trigger(dragEvents.DRAG_UPDATE, this, $handle, range, position, value);
    },

    _dispatchDragEnd: function($handle, range, position, value) {
        this.trigger(dragEvents.DRAG_END, this, $handle, range, position, value);
    }

}); // eof HorizontalSliderControl

module.exports.HorizontalSliderControl = HorizontalSliderControl;

}); // eof define
