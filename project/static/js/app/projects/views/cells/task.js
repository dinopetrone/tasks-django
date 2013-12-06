define(function(require, exports, module) {

var marionette = require('marionette');
var view = require('hbs!app/projects/templates/task');

var TaskView = marionette.ItemView.extend({
    template: view,
    className: 'task',
    tagName: 'li',

    onShow: function(){

    }

});

exports.TaskView = TaskView;

});
