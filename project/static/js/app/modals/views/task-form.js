define(function(require, exports, module) {

var $ = require('jquery');
var _ = require('underscore');
var marionette = require('marionette');
var backbone = require('backbone');
var events = require('../events');
var KeyResponder = require('built/core/responders/keys').KeyResponder;
var template = require('hbs!../templates/task-form');
var Task = require('app/projects/models/task').Task;

var TaskFormView = marionette.ItemView.extend({
    template: template,

    events: {
        'click .actions .btn.create': 'wantsCreate',
        'click .actions .btn.cancel': 'wantsCancel'
    },

    bindings: {
        'input[name="inputType"]': 'type',
        'input[name="inputLOE"]': 'levelOfEffort',
        '#inputLabel': 'label',
        '#inputDescription': 'description',
    },

    initialize: function(){
        this._data = {ok: false};
        this.model = new Task();
    },

    onRender: function(){
        _.bindAll(this, 'wantsCancelWithKeys', 'wantsCreateWithKeys');

        this.keyResponder = new KeyResponder({
            el: $(window),
            cancelOperation: this.wantsCancelWithKeys,
            acceptKeyEquivalent: true
        });

        this.keyResponder.registerKeyEquivalentWithString(
            'command + enter',
            this.wantsCreateWithKeys);

        this.stickit();
    },

    wantsCreate: function(){
        console.log(this.model.attributes);
        this._data = {ok: true, model: this.model};
        this.trigger(events.COMPLETE);
    },

    wantsCancel: function(){
        this.trigger(events.COMPLETE);
    },

    wantsCreateWithKeys: function(){
        this.keyResponder.close();
        this.keyResponder = null;
        this.wantsCreate();
    },

    wantsCancelWithKeys: function(){
        this.keyResponder.close();
        this.keyResponder = null;
        this.wantsCancel();
    },

    getData: function(){
        return this._data;
    },

    onClose: function(){
        if(this.keyResponder){
            this.keyResponder.close();
            this.keyResponder = null;
        }
    }

});

exports.TaskFormView = TaskFormView;

});


