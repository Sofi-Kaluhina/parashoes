var app = angular.module(
    "parashoesAdminApp",
    [
        'ngRoute',
        'ngAnimate',
        'ngSanitize',
        'ui.bootstrap'
    ]
);

app.config(function($routeProvider, $locationProvider){

    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');

    $routeProvider
        .when('/', {
            templateUrl: '/template/home.html',
            controller: 'MainController'
        })
        .when('/user/list', {
            templateUrl: '/template/user/list.html',
            controller: 'UserListController'
        })
        .when('/user/type', {
            templateUrl: '/template/user/type.html',
            controller: 'UserTypeController'
        })
        .when('/product/list', {
            templateUrl: '/template/product/list.html',
            controller: 'ProductListController'
        })
        .when('/product/type', {
            templateUrl: '/template/product/type.html',
            controller: 'ProductTypeController'
        })
        .when('/product/photo', {
            templateUrl: '/template/product/photo.html',
            controller: 'ProductPhotoController'
        })
        .when('/attribute/type', {
            templateUrl: '/template/attribute/type.html',
            controller: 'AttributeTypeController'
        })
        .when('/attribute/value', {
            templateUrl: '/template/attribute/value.html',
            controller: 'AttributeValueController'
        })
        .otherwise({
            redirectTo: '/'
        })
    }
);

app.run(['$rootScope', '$route', function ($rootScope, $route) {
    $rootScope.apiUrl = 'http://parashoes:8080/';
    $rootScope.baseUrl = 'api/v1/';
}]);