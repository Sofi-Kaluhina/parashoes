/**
 * Created by sofi on 15.07.16.
 */

app.controller('MainController', function ($rootScope, $http, $scope, Init) {
    $scope.mainPageProducts = [];
    $scope.currentPage = 1; // keeps track of the current page
    $scope.pageSize = 10; // holds the number of items per page

    $scope.init = function () { // initialize the sample items with some values
        $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'products')
            .success(function (response) {
                    $scope.mainPageProducts = response;
                }
            );
        $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'init')
            .success(function (response) {
                    Init.setInitialData(response.brand, response.categories_filter_conditions);
                }
            );
        };

    $scope.initialData = Init.getInitialData();
});

app.filter('start', function () {
    return function (input, start) {
        if (!input || !input.length) {
            return;
        }
        start = +start;
        return input.slice(start);
    };
});
