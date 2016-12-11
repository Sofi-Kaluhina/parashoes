/**
 * Created by sofi on 15.07.16.
 */

app.controller('MainController', function ($rootScope, $http, $scope, InitialData) {
    $scope.mainPageProducts = [];
    $scope.currentPage = 1; // keeps track of the current page
    $scope.pageSize = 10; // holds the number of items per page


    $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'products')
        .success(function (response) {
                $scope.mainPageProducts = response;
            }
        );

    InitialData.async().then(function(responce) {
        $scope.initialData = responce;
    });
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
