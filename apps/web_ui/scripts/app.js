/**
 * Created by sofi on 30.05.16.
 */
var app = angular.module(
    "bulavkaApp",
    [
        'colorbox',
        'ezplus',
        'ngRoute',
        'ui.bootstrap'
        // 'ngCart'
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
        .when('/categories/:categoryName', {
            templateUrl: '/template/categories.html',
            controller: 'CategoriesController'
        })
        .when('/product/:slug_name', {
            templateUrl: '/template/product_page.html',
            controller: 'ProductPageController'
        })
        // .when('/cart', {
        //     templateUrl: '/template/cart_view.html',
        //     controller: 'CartController'
        // })
        .otherwise({
            redirectTo: '/'
        })
    }
);

app.run(['$rootScope', '$route', function ($rootScope, $route) {
    $rootScope.apiUrl = 'http://bulavka:8080/';
    $rootScope.baseUrl = 'api/v1/';
}]);

app.factory('InitialData', function ($rootScope, $http) {
    var initialData = {
        brand: {},
        categoriesFilterCondition: {}
    };

    $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'init')
        .success(function (response) {
                initialData.brand = response.brand;
                initialData.categoriesFilterCondition = response.categories_filter_conditions;
            }
        );

    return initialData
});