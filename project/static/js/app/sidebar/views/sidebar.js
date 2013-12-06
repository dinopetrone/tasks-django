define(function(require, exports, module) {

var marionette = require('marionette');
var backbone = require('backbone');
var ProjectDetailView = require('app/projects/views/details').ProjectDetailView;
var FooterView = require('./footer').FooterView;
var ProjectListView = require('./projects').ProjectListView;
var Project = require('../models/projects').Project;
var view = require('hbs!app/sidebar/templates/sidebar');

// this is probably better as a layout.

var SidebarView = marionette.ItemView.extend({
    template: view,
    className: 'view',
    projectDetailRegion: null,

    ui: {
        projectListView: '.menu',
        footerView: '.footer'
    },

    initialize: function(options){
        this.projectDetailRegion = options.projectDetailRegion;
    },

    wantsAddProject: function(){
        this.addNewProject();
    },

    wantsRemoveProject: function(){
        this.removeCurrentProject();
    },

    wantsSelectProject: function(sender, projectView){
        this.showProject(projectView.model);
    },

    wantsToggleProjects: function(){
        if(this.$el.parent().hasClass('hide')){
            this.showProjectsPane(true);
        } else {
            this.showProjectsPane(false);
        }
    },

    showProjectsPane: function(bool){
        if(bool){
            this.$el.parent().removeClass('hide');
            return;
        }

        this.$el.parent().addClass('hide');
    },

    removeCurrentProject: function(){
        var activeProject = this.projectListView.activeProject;

        if(activeProject){
            this.projectListView.projects.collection.remove(activeProject.model);
            this.projectListView.activeProject = null;

            this.stopListening(this.currentDetail, 'projects:toggle', this.wantsToggleProjects);

            this.projectDetailRegion.close();
            this.currentDetail = null;
        }
    },

    showProject: function(model){
        var projectDetailView = new ProjectDetailView({model: model});

        if (this.currentDetail){
            this.stopListening(this.currentDetail, 'projects:toggle', this.wantsToggleProjects);
        }

        this.projectDetailRegion.show(projectDetailView);
        this.currentDetail = projectDetailView;
        this.listenTo(projectDetailView, 'projects:toggle', this.wantsToggleProjects);
    },

    addNewProject: function(){
        var obj = new Project({
            projectName: 'New Project'
        });

        this.projectListView.projects.collection.add(obj);
    },

    initializeProjectList: function(){
        this.projectListView = new ProjectListView({
            el: this.ui.projectListView
        });

        this.projectListView.bindUIElements();
        this.projectListView.triggerMethod('show', this.projectListView);

        this.listenTo(this.projectListView, 'project:select', this.wantsSelectProject);
    },

    initializeFooter: function(){
        this.footerView = new FooterView({
            el: this.ui.footerView
        });

        this.footerView.bindUIElements();
        this.footerView.triggerMethod('show', this.footerView);

        this.listenTo(this.footerView, 'project:add', this.wantsAddProject);
        this.listenTo(this.footerView, 'project:remove', this.wantsRemoveProject);
    },

    onShow: function(){
        this.initializeFooter();
        this.initializeProjectList();
    }

});

exports.SidebarView = SidebarView;

});
