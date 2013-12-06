define(function(require, exports, module){

// Imports

var _ = require('underscore');
var getElement = require('built/ui/helpers/dom').getElement;


// Helper functions
function registerElement(value, required){
    var idKey = 'auf-id';

    required = _.isUndefined(required) ? true : required;
    if(required && !value) throw 'No input element provided.';

    var $el = getElement(value);

    _.each($el, function(each){
        $target = $(each);

        if(!$target.data(idKey)){
            $target.data(idKey, _.uniqueId());
        }
    });

    return $el;
}

function getElementId($el){
    var idKey = 'auf-id';
    return $el.data(idKey);
}

/**
 * compose a function from one module to another and maintain original module scope.
 * @param  {object} intoScope the scope you wish to compose the method into
 * @param  {object} fromScope the scope you wish to retrieve the method from
 * @param  {string} func      the function name, as a string
 * @return {undefined}
 *
 * @example
 * compose(this, fooModule, 'fooModuleMethod');
 */
function compose (intoScope, fromScope, func) {
    intoScope[func] = _.bind(fromScope[func], fromScope);
}

/**
 * Identical to compose, but takes list of n-function names.
 * @param  {object} intoScope the scope you wish to compose the method into
 * @param  {object} fromScope the scope you wish to retrieve the method from
 * @return {undefined}
 *
 * @example
 * composeAll(
 *     this,
 *     fooModule,
 *     'fooModuleMethod1',
 *     'fooModuleMethod2',
 *     'fooModuleMethod3'
 * );
 */
function composeAll(intoScope, fromScope) {
    var args;

    function iterator(func, i, funcs) {
        compose(intoScope, fromScope, func);
    }

    funcs = Array.prototype.slice.call(arguments, 2);

    _.each(funcs, iterator);
}

/**
 * normalizes an integer against a min and max
 * @param  {int} value the value you wish to normalize
 * @param  {int} min   the value's min limit
 * @param  {int} max   the value's max limit
 * @return {int}       normalized integer
 */
function normalizeInt(value, min, max) {
    // Ternary is faster than Math.min|max
    value = value > max ? max : value;
    value = value < min ? min : value;

    return value;
}

function sortArrayAscending(a, b) {
    // see: http://bit.ly/1c0cPTU
    return a - b;
}

function mixins(Source, Destination){
    names = Array.prototype.slice.call(arguments, 2);
    _.each(names, function(name){
        Destination.prototype[name] = function(){
            return Source.prototype[name].apply(this, arguments);
        };
    });
}

// Exports

exports.compose            = compose;
exports.composeAll         = composeAll;
exports.normalizeInt       = normalizeInt;
exports.sortArrayAscending = sortArrayAscending;
exports.sortArrayAscending = sortArrayAscending;
exports.registerElement    = registerElement;
exports.getElementId       = getElementId;
exports.mixins              = mixins;
});
