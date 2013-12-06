define(function(require, exports, module) {

var ApplicationDelegate = require('./delegate').ApplicationDelegate;
var ModalRegion = require('app/modals/region').ModalRegion;

function main(options){
    var app = this;
    app.addRegions({
        window: '#window',
        sidebar: '#sidebar',
        modal: ModalRegion,
        projectDetail: '#project-detail'
    });

    new ApplicationDelegate({app: app});
}

exports.main = main;
});

