/**
 * Created by sofi on 15.07.16.
 */

app.controller('MainController', function($scope, $http) {
    $scope.items = [];


    $http.get('http://bulavka:8080/api/v1/products')
        .success(function(responce) {
            $scope.items = responce;
            console.log(responce);
            console.log("hi");
        }
    );

});