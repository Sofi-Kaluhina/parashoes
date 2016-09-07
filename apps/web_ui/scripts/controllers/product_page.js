/**
 * Created by markel on 25.08.16.
 */

app.controller('ProductPageController', function ($rootScope, $http, $scope, $routeParams) {
    $scope.product = [];

    var current_id = $routeParams.id;

    $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'product/' + current_id)
        .success(function(responce) {
            $scope.product = responce;
        }
    );

    $scope.info = "product-info";

    $scope.class = "zoom-out";

    $scope.changeClass = function() {
        if ($scope.class === "zoom-out" && $scope.info === "product-info") {
            $scope.class = "zoom-in";
            $scope.info = "when-zoom-in";
            }
        else {
            $scope.class = "zoom-out";
            $scope.info = "product-info";
        }
    };




});

