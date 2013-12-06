define(function(require, exports, module) {

var backbone = require('backbone');

var Project = backbone.Model.extend({
    projectName: null
});

exports.Project = Project;

});
