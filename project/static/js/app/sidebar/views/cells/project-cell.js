define(function(require, exports, module) {

var marionette = require('marionette');
var $ = require('jquery');
var _ = require('underscore');
var KeyResponder = require('built/core/responders/keys').KeyResponder;
var view = require('hbs!app/sidebar/templates/project-cell');


var ProjectCell = marionette.ItemView.extend({
    template: view,
    tagName: 'li',
    className: 'project-cell',

    events: {
        'click label': 'wantsStartEditing',
        'click': 'wantsSelect'
    },

    ui: {
        label: 'label',
        input: 'input'
    },

    onRender: function(){
        _.bindAll(this, 'wantsEndEditing', 'wantsCancelEditing');
        this.ui.input.on('blur', this.wantsCancelEditing);
        this._selected = false;
    },

    setSelected: function(bool){

        if(bool){
            this.$el.addClass('selected');
        } else {
            this.$el.removeClass('selected');
        }

        this._selected = bool;
    },

    wantsSelect: function(e){
        if (this._selected === false){
            this.trigger('select', this);
        }
    },

    wantsStartEditing: function(){
        if (this._selected){
            this.startEditing();
        }
    },

    wantsCancelEditing: function(){
        this.endEditing();
    },

    wantsEndEditing: function(){
        this.endEditing(this.ui.input.val());
    },

    startEditing: function(){
        this.trigger('edit:start', this);

        var label = this.ui.label;
        var input = this.ui.input;

        label.hide();

        this.keyResponder = new KeyResponder({
            el: this.ui.input,
            cancelOperation: this.wantsCancelEditing,
            insertNewline: this.wantsEndEditing
        });

        input.val(label.text());
        input.show();
        input[0].focus();
    },

    endEditing: function(value){
        value = $.trim(value);
        this.trigger('edit:end', this, value);

        var label = this.ui.label;
        var input = this.ui.input;

        if(this.keyResponder){
            this.keyResponder.close();
        }

        if(!_.isEmpty(value)){
            label.text(value);
            this.model.set('projectName', value);
        }

        input.hide();
        label.show();
    }

});

exports.ProjectCell = ProjectCell;

});
