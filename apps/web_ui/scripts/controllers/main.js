/**
 * Created by sofi on 15.07.16.
 */

app.controller('MainController', function ($rootScope, $http, $scope) {
    $scope.items = [];

    //console.log($rootScope.apiUrl + $rootScope.baseUrl + 'products');

    $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'products')
        .success(function(responce) {
            $scope.items = responce;
        }
    );

});