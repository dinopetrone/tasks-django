define(function (require, exports, module) {

var marionette = require('marionette');
var getElementId = require('built/core/utils/helpers').getElementId;
var DragDropList = require('built/core/controls/dragdrop/list').DragDropList;


var DragAndDropCollectionView =  marionette.CollectionView.extend({
    initialize: function(options){
        options = _.extend({dataType:'com.built.generic'}, options);

        _.bindAll(this,
                'getDragImage',
                'getDragDataForElement',
                'renderPlaceholderForData',
                'dropResponderPerformDragOperation',
                'draggingEndedRestoreElementAtPosition'
                );
        this.dragDropList = new DragDropList({
            getDragImage: this.getDragImage,
            getDragDataForElement: this.getDragDataForElement,
            renderPlaceholderForData: this.renderPlaceholderForData,
            dropResponderPerformDragOperation: this.dropResponderPerformDragOperation,
            draggingEndedRestoreElementAtPosition: this.draggingEndedRestoreElementAtPosition,
            dataType:options.dataType
        });
        this.dragDropList.setDropElement(this.$el);
        this.on('show', this.onShow);
    },

    onClose: function(){
        this.dragDropList.close();
    },

    onShow: function(){

    },


    getViewForEl: function($el){
        return this.getViewForId(getElementId($el));
    },

    getDragImage: function(){
        return false;
    },

    renderPlaceholderForData: function(){
        throw 'renderPlaceholderForData Not Implemented';
    },

    getViewForId: function(id){
        var output;
        this.children.each(function(view){
            if(getElementId(view.$el) == id){
                output = view;
            }
        });
        return output;
    },

    getDragDataForElement: function($el){
        var view = this.getViewForEl($el);
        var model = view.model;
        this.collection.remove(model, {silent:true});
        return this.serializeModel(model);
    },

    serializeModel: function(model){
        return JSON.stringify(model.toJSON());
    },

    deserializeModel: function(data){
        return $.parseJSON(data);
    },

    dropResponderPerformDragOperation: function(responder, e){
        var model = this.deserializeModel(responder.getData());
        var position = this.dragDropList._placeholderIndex;
        this.dragDropList.removePlaceholder();
        this.collection.add(model,{at:position});
    },

    draggingEndedRestoreElementAtPosition: function(position, $el){
        var model = this.getViewForEl($el).model.toJSON();
        this.collection.add(model,{at:position});
    },

    appendHtml: function(collectionView, itemView, index){
        this.dragDropList.insertDragElement(index, itemView.$el);
    },

});

exports.DragAndDropCollectionView = DragAndDropCollectionView;

});
