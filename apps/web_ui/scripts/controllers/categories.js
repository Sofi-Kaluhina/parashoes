/**
 * Created by sofi on 06.11.16.
 */

app.controller('CategoriesController', function ($rootScope, $scope, filterFilter, $http, $routeParams, Init) {
    var _response = [];
    $scope.categoriesPageProducts = [];
    $scope.categoriesFilterCondition = [];
    $scope.categories = [];
    $scope.Filter = new Object();
    $scope.currentCategoryName = $routeParams.categoryName;

    $http({
        method: 'POST',
        url: $rootScope.apiUrl + $rootScope.baseUrl + 'categories',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        },
        data: {
            categories_filter_conditions: Init.getInitialData().categoriesFilterCondition[$scope.currentCategoryName]
        }
    }).success(function (response) {
            $scope.categoriesPageProducts = response;
            // _response.push(response);
            // _response.forEach(function (element) {
            //     $scope.categoriesProducts.push(element.products);
            //     $scope.categories.push(element.attributes)
            // });
            // $scope.categories.forEach(function (element) {
            //     Object.keys(element).forEach(function (season) {
            //         $scope.Filter.season = element[season]
            //     });
            // });
        }
    );

    $http.get('../json/categories_data_model_example.json')
        .success(function (response) {

            $scope.categoriesFilterCondition = response.attributes;
        })
});