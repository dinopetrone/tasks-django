define(function(require, exports, module){

// Imports

var Marionette = require('marionette');
var _          = require('underscore');
var helpers    = require('built/core/utils/helpers');

// Module
var DropResponder = Marionette.Controller.extend({

    // Object vars
    el: null,
    dataType: 'com.built.generic',

    // operation can be one of:
    // -    'none'
    // -    'copy'
    // -    'move'
    // -    'link'
    // -    'copyMove'
    // -    'copyLink'
    // -    'linkMove'
    // -    'all'
    operation: 'all',

    // Initialization
    initialize: function(options){
        _.extend(this, options);
        _.bindAll(this,
            '_dragOver', '_dragEnter', '_dragLeave', '_drop',
            'shouldAllowDrop');

        this.$el = helpers.registerElement(this.el);

        this.$el.on('dragenter.built.responders.drop', {ctx: this}, this._dragEnter);
        this.$el.on('dragover.built.responders.drop', {ctx: this}, this._dragOver);
        this.$el.on('dragleave.built.responders.drop', {ctx: this}, this._dragLeave);
        this.$el.on('drop.built.responders.drop', {ctx: this}, this._drop);

    },

    _dragEnter: function(e){
        this._updateMousePosition(e);

        if (!this.shouldAllowDrop(this, e)){
            return;
        }

        e.preventDefault();
        this.draggingEntered(this, e);
    },

    _dragOver: function(e){
        this._updateMousePosition(e);

        if (!this.shouldAllowDrop(this, e)){
            return;
        }

        e.preventDefault();
        this.draggingUpdated(this, e);
    },

    _dragLeave: function(e){
        this._updateMousePosition(e);
        this.draggingExited(this, e);
    },

    _drop: function(e){
        // prevent the browser from handling the drop
        if (e.stopPropagation) e.stopPropagation();
        if (e.preventDefault) e.preventDefault();

        var originalEvent = e.originalEvent;
        var dataTransfer = originalEvent.dataTransfer;

        this._setData(dataTransfer.getData(this.dataType));
        this.performDragOperation(this, e);
    },

    shouldAllowDrop: function(responder, e){
        var originalEvent = e.originalEvent;
        var dataTransfer = originalEvent.dataTransfer;

        //event.dataTransfer.dropEffect = "copy";
        var result = false;
        if (this.operation != 'all' &&
            dataTransfer.effectAllowed != 'all' &&  // here for safari.
            dataTransfer.effectAllowed != this.operation){
            return result;
        }

        if(_.isArray(this.dataType)){
            _.each(this.dataType, function(each){
                var index = _.indexOf(dataTransfer.types, each);

                if(index !== -1){
                    result = true;
                }
            });

        } else {
            var index = _.indexOf(dataTransfer.types, this.dataType);
            if(index !== -1){
                result = true;
            }
        }

        return result;
    },

    _updateMousePosition: function (e){

        var positionX = e.originalEvent.pageX;
        var positionY = e.originalEvent.pageY;

        this._setMousePosition(positionX, positionY);
    },

    _setMousePosition: function(x, y){
        this._position = {x: x, y: y};
    },

    getMousePosition: function(){
        return this._position;
    },

    _setData: function(data){
        this._data = data;
    },

    getData: function(){
        return this._data;
    },

    draggingEntered: function(responder, e){},
    draggingUpdated: function(responder, e){},
    draggingExited: function(responder, e){},
    performDragOperation: function(responder, e){},

    // Marionette overrides

    onClose: function(){
        this.$el.off('dragenter.built.responders.drop', this._dragEnter);
        this.$el.off('dragover.built.responders.drop', this._dragOver);
        this.$el.off('dragleave.built.responders.drop', this._dragLeave);
        this.$el.off('drop.built.responders.drop', this._drop);
    }

}); // eof DropResponder

// Exports

exports.DropResponder = DropResponder;

}); // eof define
