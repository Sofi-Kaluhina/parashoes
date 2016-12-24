/**
 * Created by sofi on 30.05.16.
 */
var app = angular.module(
    "bulavkaApp",
    [
        'colorbox',
        'ezplus',
        'ngRoute',
        'ui.bootstrap',
        'ngCart'
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
        .when('/feedback', {
            templateUrl: '/template/feedback.html',
            controller: 'FeedbackController'
        })
        .when('/categories/:categoryName', {
            templateUrl: '/template/categories.html',
            controller: 'CategoriesController',
            reloadOnSearch: false
        })
        .when('/product/:slug_name', {
            templateUrl: '/template/product_page.html',
            controller: 'ProductPageController'
        })
        .when('/cart', {
            templateUrl: '/template/cart_view.html',
            controller: 'CartController'
        })
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
    // фабрика возвращает объект, в котором под ключем async ф-ция,
    // которая возвращает промис от http-запроса,
    // который возвращает data.brand и data.categories_filter_conditions
    // которые записываются в этот объект с ключами brand и categoriesFilterCondition
    var initialData = {
        async: function() {
            var promise = $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'init')
                .then(function (response) {
                    return {
                        brand: response.data.brand,
                        categoriesFilterCondition: response.data.categories_filter_conditions
                    };
                }
            );
            return promise;
        }
    };
    return initialData;
});
