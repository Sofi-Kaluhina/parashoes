/**
 * Created by sofi on 06.11.16.
 */

app.controller('CategoriesController', function ($rootScope, $scope, $http, $routeParams, $location, $timeout, InitialData) {
    $scope.categoriesPage = {};
    $scope.categoriesFilterCondition = [];
    $scope.categories = [];
    $scope.Filter = new Object();
    $scope.categoriesFilterModel = {checkbox: []};

    var currentCategoryName = '';

    if ($routeParams.categoryName) {
        currentCategoryName = $routeParams.categoryName;
    } else {
        currentCategoryName = $location.path().split('/')[2];
    }

    var getContent = function (filtersIds, itemName) {
        $http({
            method: 'POST',
            url: $rootScope.apiUrl + $rootScope.baseUrl + 'categories',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            },
            data: {
                categories_filter_conditions: filtersIds
            }
        }).success(function (response) {
                $scope.categoriesPage[itemName] = response[itemName];
            }
        );
    };

    InitialData.async().then(function (responce) {
        $scope.filtersIdsQueryString = $location.search()['f'];
        $scope.filtersIds = responce['categoriesFilterCondition'][currentCategoryName];
        var filterIdsQueryStringValidation = function () {
            if ($scope.filtersIdsQueryString) {
                if (typeof $scope.filtersIdsQueryString == 'string') {
                    $scope.filtersIdsQueryString = [parseInt($scope.filtersIdsQueryString)];
                } else if (typeof $scope.filtersIdsQueryString == 'undefined') {
                    $scope.filtersIdsQueryString = [];
                }
            } else {
                $scope.filtersIdsQueryString = [$scope.filtersIds[0]]
            }
        };

        filterIdsQueryStringValidation();

        $scope.filtersIdsQueryString.forEach(function (element) {
            if (!$scope.filtersIds.includes(parseInt(element))) {
                $scope.filtersIds.push(parseInt(element));
            }
        });

        getContent($scope.filtersIds, 'products');
        getContent([$scope.filtersIds[0]], 'filters');

        filterIdsQueryStringValidation();

        $scope.filtersIdsQueryString.forEach(function (element) {
            if (!$scope.categoriesFilterModel.checkbox.includes(parseInt(element))) {
                $scope.categoriesFilterModel.checkbox[element] = true
            }
        });
    });

    $scope.filterCheck = function () {
        var checkboxes = document.getElementsByClassName('filter-checkbox');
        var mainCondition = [$scope.filtersIds[0]];
        for (var i = 0; i < checkboxes.length; ++i) {
            $scope.filtersIds = mainCondition;
            if (checkboxes[i].checked) {
                $scope.filtersIds.push(parseInt(checkboxes[i].id));
            }
        }
        $location.search('f', $scope.filtersIds);
        getContent($scope.filtersIds, 'products');
    };

    $scope.isFilterChecked = function (filterId) {
        return !!$scope.filtersIds.includes(filterId);
    }
});
