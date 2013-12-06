define(function(require, exports, module) {

var marionette = require('marionette');
var _ = require('underscore');

var ModalRegion = marionette.Region.extend({
    el: '#modal',

    open: function(view){
        marionette.Region.prototype.open.call(this, view);
        this.$el.show();

        // can't use _.defer here for Chrome.
        // there is an issue where it appears as though
        // the defer is not defered at all, but happens immediately.
        // Though the call to _.defer does work in Safari.
        // Anyway, the setTimeout here fixes the issue.

        setTimeout(function(){
            view.$el.addClass('show');
        }, 15);
    },

    // Close the current view, if there is one. If there is no
    // current view, it does nothing and returns immediately.
    close: function(){
        var view = this.currentView;
        if (!view || view.isClosed){ return; }

        var self = this;
        view.$el.removeClass('show');

        setTimeout(function(){
            marionette.Region.prototype.close.call(self);
            self.$el.hide();
        }, 200);
    }
});


exports.ModalRegion = ModalRegion;

});
