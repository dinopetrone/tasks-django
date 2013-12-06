/*
    the projects require.js config,
    used in build process also
    see: http://requirejs.org/docs/api.html#config
*/

/*global requirejs*/
requirejs.config({
    waitSeconds: 30,
    shim: {
        'modernizr': { exports: 'Modernizr' },
        'underscore': { exports: '_' },
        'backbone': { deps: ['underscore','jquery'], exports: 'Backbone' },
        'backbone.tastypie': { deps: ['backbone','jquery','jquery.timeago'], exports: 'Backbone' },
        'marionette' : { deps : ['backbone'], exports : 'Backbone.Marionette'},
        'twitter-text': { exports: 'twttr' },
        'jquery': { exports: '$' },
        'flowtype': { exports: '$', deps : ['jquery'] },
        'jquery.timeago': { exports: '$',deps : ['jquery'] },
        'jquery.inview': { exports: '$', deps : ['jquery'] },
        'jquery.social' : {exports: '$',deps: ['jquery']},
        'video': { exports: 'video' },
        'youtube' : {exports: 'YT'},
        'facebook' : {
            exports: 'FB',
            init: function(){
                var FBAppID;
                if (document.location.href.indexOf('localhost') > -1) {
                    //localhost
                    FBAppID = '154262331438956';
                } else {
                    //production
                    FBAppID = '1423597031185864';
                }
                this.FB.init({
                    appId: FBAppID,
                    xfbml: true
                });
                return this.FB;
            }
        }
    },
    //re-route libs to top-level
    paths: {
        'jquery': 'libs/jquery',
        'jquery.timeago': 'libs/jquery.timeago',
        'jquery.inview': 'libs/jquery.inview',
        'jquery.social': 'libs/jquery.social',
        'backbone': 'libs/backbone',
        'backbone.tastypie': 'libs/backbone.tastypie',
        'marionette' : 'libs/backbone.marionette',
        'underscore': 'libs/underscore',
        'text': 'libs/text',
        'flowtype': 'libs/flowtype',
        'tpl' : 'libs/tpl',
        'domReady': 'libs/domReady',
        'modernizr': 'libs/modernizr',
        'waypoints': 'libs/waypoints',
        'twitter-text': 'libs/twitter-text',
        'video': 'libs/video',
        'facebook': '//connect.facebook.net/en_US/all.js?',
        'twitter': '//platform.twitter.com/widgets.js?',
        'youtube': '//www.youtube.com/player_api?'
    }
});