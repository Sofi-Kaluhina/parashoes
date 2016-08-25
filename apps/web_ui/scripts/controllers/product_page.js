/**
 * Created by markel on 25.08.16.
 */

app.controller('ProductPageController', function ($rootScope, $http, $scope, $routeParams) {
    $scope.product = [];

    var current_id = $routeParams.id;

    console.log($rootScope.apiUrl + $rootScope.baseUrl + 'product/' + current_id);

    $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'product/' + current_id)
        .success(function(responce) {
            $scope.product = responce;
        }
    );

    $scope.zoomIn = function () {
        console.log("mouse over on photo")
    }

});
