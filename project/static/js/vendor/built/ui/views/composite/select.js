define(function (require, exports, module) {

var marionette = require('marionette');

var Select = require('built/core/controls/forms/select').Select;
var helpers = require('built/core/utils/helpers');
var focus = require('built/core/events/focus');
var event = require('built/core/events/event');
var modelFromElements = require('built/ui/helpers/dom').modelFromElements;

require('stickit');

var SelectCompositeView = marionette.CompositeView.extend({
    events:{
        'click .btn':'onOpenPress'
    },
    initialize : function(options){
        _.extend(this, options);
        _.bindAll(this,
            'hideList',
            'showList',
            'searchForText');
        this.model = new Backbone.Model();
        this.listenToOnce(this.model, 'change', this.onModelChange);
        this.select = new Select({
            $el:this.$el,
            hideList:this.hideList,
            showList:this.showList,
            searchForText:this.searchForText,
        });
        this.listenTo(this.select, focus.FOCUS, this.onOptionFocus);
        this.listenTo(this.select, focus.BLUR, this.onOptionBlur);
        this.listenTo(this.select, event.SELECT , this.onOptionSelected);
        this.listenTo(this.model, 'change', this._onModelChange);
    },

    onShow: function(){
        var elements = [];
        var views = this.children.toArray();
        _.each(views, function(each){
            elements.push(each.$el[0]);
        });
        this.select.setElements($(elements));
        var marionetteDict = this.marionetteDict = {};
        _.each(views, function(each){
            var key = helpers.getElementId(each.$el);
            marionetteDict[key] = each;
        });
        this.hideList();
    },

    _onModelChange: function(){
        var selected = this.collection.where(this.model.toJSON())[0];
        var child = this.children.findByModel(selected);
        if(this._selectedChild){
            this._selectedChild.trigger(event.DESELECT);
        }
        this._selectedChild = child;
        child.trigger(event.SELECT);
    },

    hideList: function(){
        this.ui.list.hide();
    },

    showList: function(){
        this.ui.list.show();
    },

    searchForText: function(label){
        label = label.toLowerCase();
        var coll = this.children.toArray();
        var lowestIndex = null;
        var view;
        for(var i=0; i < coll.length; i ++){
            view = coll[i];
            var model = view.model;
            var index = model.get('value').indexOf(label);

            if(index === 0){
                break;
            }
            view = null;
        }
        if(view){
            this.select.focusManager.focus(view.$el[0]);
            // this.select.setSelectedOption(view.$el[0]);
        }
    },

    onOptionFocus: function(sender, obj){
        var key = helpers.getElementId($(obj));
        var view = this.marionetteDict[key];
        view.trigger(focus.FOCUS);
    },

    onOptionBlur: function(sender, obj){
        var key = helpers.getElementId($(obj));
        var view = this.marionetteDict[key];
        view.trigger(focus.BLUR);
    },

    onOptionSelected: function($el){
        var key = helpers.getElementId($el);
        var view = this.marionetteDict[key];
        var model = view.model;
        this.model.set(view.model.toJSON());
    },

    onModelChange: function(){
        this.stickit();
    },

});

function selectFromSelect(SelectClass, $select, options){

    options = options || {};
    var selectData = modelFromElements($select.find('option').toArray(), null, {content:'option'});
    var selectCollection = new Backbone.Collection(selectData);
    options = _.extend(options,{collection:selectCollection});
    var createdSelect = new SelectClass(options);
    $select.hide();

    createdSelect.model.on('change', function(){
        var val = this.get('value');
        $select.val(val);
    });

    $select.on('change', function(){
        var selectedVal = $select.val();
        var model = selectCollection.where({value:selectedVal})[0];
        createdSelect.model.set(model.toJSON());
    });



    return createdSelect;
}

exports.SelectCompositeView = SelectCompositeView;
exports.selectFromSelect = selectFromSelect;

});
