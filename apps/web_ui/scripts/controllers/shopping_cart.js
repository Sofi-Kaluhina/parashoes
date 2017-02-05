/**
 * Created by sofi on 23.11.16.
 */

app.controller ('CartController', ['$scope', '$http', 'ngCart', function($scope, $http, ngCart) {
    ngCart.setTaxRate(7.5);
    ngCart.setShipping(2.99);
}]);
