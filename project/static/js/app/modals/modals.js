define(function(require, exports, module) {

var vent = require('app/vent').vent;
var events = require('./events');
var ModalView = require('./views/modal').ModalView;

var currentModal = null;


function presentModal(view){

    // only 1 modal at a time please.
    if(currentModal) return;

    currentModal = new ModalView({itemView: view});
    vent.trigger(events.PRESENT, currentModal);
    return currentModal;
}

function dismissModal(){
    vent.trigger(events.DISMISS, currentModal);
    currentModal = null;
}

exports.presentModal = presentModal;
exports.dismissModal = dismissModal;
});
