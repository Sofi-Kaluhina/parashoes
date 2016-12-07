/**
 * Created by sofi on 06.11.16.
 */

app.controller('CategoriesController', function ($rootScope, $scope, $http, $routeParams, $location, $timeout, InitialData) {
    $scope.categoriesPage = {};
    $scope.categoriesFilterCondition = [];
    $scope.categories = [];
    $scope.Filter = new Object();

    var currentCategoryName = '';

    if ($routeParams.categoryName) {
        currentCategoryName = $routeParams.categoryName;
    } else {
        currentCategoryName = $location.path().split('/')[2];
    }

    $scope.filtersIds = InitialData.categoriesFilterCondition[currentCategoryName] || [];

    var getContent = function () {
        $http({
            method: 'POST',
            url: $rootScope.apiUrl + $rootScope.baseUrl + 'categories',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            },
            data: {
                categories_filter_conditions: $scope.filtersIds
            }
        }).success(function (response) {
                $scope.categoriesPage.products = response.products;
                $scope.categoriesPage.filters = response.filters;
                return $scope.categoriesPage;
            }
        );
    };

    getContent();

    $scope.filterCheck = function () {
        var checkboxes = document.getElementsByClassName('filter-checkbox');
        for (var i = 0; i < checkboxes.length; ++i) {
            if (checkboxes[i].checked) {
                $scope.filtersIds.push(parseInt(checkboxes[i].id))
            }
        }
        console.log($scope.filtersIds);
        $timeout(function () {
            getContent();
            $scope.$apply();
        }, 100);
    }

});