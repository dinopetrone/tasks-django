define(function(require, exports, module){

var _ = require('underscore');
var cssPointer = require('built/core/features/css-pointer-events');


function supressChildPointerEvents($el){
    // http://jsfiddle.net/theodorejb/j2fDt/9/

    var targets = [];

    if (cssPointer.supported()){
        $el.find('*').css({'pointer-events': 'none'});
        targets = $el;

    } else {
        $el.add($el.find('*'));
        targets = $el;
    }

    _.each(targets, function(each){
        $target = $(each);
        $target.on('dragenter.built.responders.drop', _supressEventHandler);
        $target.on('dragleave.built.responders.drop', _supressEventHandler);

    });

    return $el;
}

function clearSupressedPointerEvents($el){

    if (cssPointer.supported()){
        $el.find('*').css({'pointer-events': 'all'});
        targets = $el;

    } else {
        $el.add($el.find('*'));
        targets = $el;
    }

    _.each(targets, function(each){
        $target = $(each);
        $target.off('dragenter.built.responders.drop', _supressEventHandler);
        $target.off('dragleave.built.responders.drop', _supressEventHandler);

    });

    return $el;
}

function _supressEventHandler(e){

    if(!e) var e = window.event;

    // e.cancelBubble is supported by IE8 -
    // this will kill the bubbling process.
    e.cancelBubble = true;
    e.returnValue = false;

    // e.stopPropagation works in modern browsers
    if (e.stopPropagation) e.stopPropagation();
    if (e.preventDefault) e.preventDefault();
}

// Exports

exports.supressChildPointerEvents = supressChildPointerEvents;
exports.clearSupressedPointerEvents = clearSupressedPointerEvents;
});

