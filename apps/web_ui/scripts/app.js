/**
 * Created by sofi on 30.05.16.
 */
var app = angular.module("bulavkaApp", ['ngRoute']);

app.config(function($routeProvider, $locationProvider){

        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
        });

        $routeProvider
            .when('/', {
                templateUrl: '/template/home.html',
                controller: 'MainController',
                useAsDefault: true

            })
            .when('/about_us', {
                templateUrl: '/template/about_us.html',
                controller: 'AboutController'

            })
            .when('/articles', {
                templateUrl: '/template/articles.html',
                controller: 'ArticlesController'

            })
            .when('/contacts', {
                templateUrl: '/template/contacts.html',
                controller: 'ContactsController'

            })
            .otherwise({
                redirectTo: '/'
            }
        )
    }
);

app.controller('MainController', function($scope, $http) {
    $scope.items = [];


    $http.get('http://bulavka:8080/api/v1/products')
        .success(function(responce) {
            $scope.items = responce;
        }
    );

});

app.controller('ContactsController', function($scope, $http) {
    $scope.items = [];


    $http.get('./scripts/json/item-example.json')
        .success(function(responce) {
            $scope.items = responce;
        }
    );

});

app.controller('ArticlesController', function($scope, $http) {
    $scope.items = [];


    $http.get('./scripts/json/item-example.json')
        .success(function(responce) {
            $scope.items = responce;
        }
    );

});

app.controller('AboutController', function($scope, $http) {
    $scope.items = [];


    $http.get('./scripts/json/item-example.json')
        .success(function(responce) {
            $scope.items = responce;
        }
    );

});
