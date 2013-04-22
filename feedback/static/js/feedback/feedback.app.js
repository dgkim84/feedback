define(['feedback/controllers'], function(controllers) {
  angular.module('feedback', ['ngSanitize', 'ngCookies'])
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
      $locationProvider.html5Mode(true);
      $routeProvider.when('/projects', {
        templateUrl: '/static/templates/index.html',
        controller: controllers.FeedbackCtrls
      }).when('/projects/:id', {
        templateUrl: '/static/templates/index.html',
        controller: controllers.FeedbackCtrls
      }).when('/tickets/new', {
        templateUrl: '/static/templates/tickets/new.html',
        controller: controllers.FeedbackCtrls
      }).otherwise({
        redirectTo: '/projects'
      })
    }])
});