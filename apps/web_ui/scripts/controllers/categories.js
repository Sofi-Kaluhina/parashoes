/**
 * Created by sofi on 06.11.16.
 */

app.controller('CategoriesController', function ($rootScope, $scope, $http, $routeParams, $location, InitialData) {
    $scope.categoriesPage = {}; // главный обьект для рендеринга страницы категорий
    $scope.categoriesFilterModel = {checkbox: []}; // scope of all checkboxes set of filters model

    var getCurrentCategoryName = (function () {
        // чтобы контроллер понимал, откуда зашли на страницу

        if ($routeParams.categoryName) {
            // с главного экрана приложения
            return $routeParams.categoryName;
        } else {
            // или напрямую
            return $location.path().split('/')[2];
        }
    })();

    var getContent = function (filtersIds, itemName) {
        /*
        * ф-ция для отправки запроса контроллера для получения фильтров и товаров
        * @param {array} filtersIds - массив с идентификаторами фильтров (чекбоксов)
        * @param {string} itemName - или "products", или "filters", в зависимости от того, что нужно получить
         */
        $http({
            method: 'POST',
            url: $rootScope.apiUrl + $rootScope.baseUrl + 'categories',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            },
            data: {
                categories_filter_conditions: filtersIds
                // отсылая массив с id фильтров
            }
        }).success(function (response) {
                $scope.categoriesPage[itemName] = response[itemName];
            // получаем или products, или filters в репитеры для обновления или товаров или фильтров
            }
        );
    };

    InitialData.async().then(function (responce) {
        // вызываем нашу фабрику, получаем обьект с брендами и условиями фильтров
        var filtersIdsQueryString = $location.search()['f'];
        // этот метод ищет в кверистринге все значения f и, если их больше 1, записывает в массив
        $scope.filtersIds = responce['categoriesFilterCondition'][getCurrentCategoryName];
        var filterIdsQueryStringValidation = function () {
            if (filtersIdsQueryString) {
                if (typeof filtersIdsQueryString == 'string') {
                    filtersIdsQueryString = [parseInt(filtersIdsQueryString)];
                } else if (typeof filtersIdsQueryString == 'undefined') {
                    filtersIdsQueryString = [];
                }
            } else {
                filtersIdsQueryString = [$scope.filtersIds[0]]
            }
        };

        filterIdsQueryStringValidation();

        filtersIdsQueryString.forEach(function (element) {
            if (!$scope.filtersIds.includes(parseInt(element))) {
                $scope.filtersIds.push(parseInt(element));
            }
        });

        getContent($scope.filtersIds, 'products');
        getContent([$scope.filtersIds[0]], 'filters');

        filterIdsQueryStringValidation();

        filtersIdsQueryString.forEach(function (element) {
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
        // getContent($scope.filtersIds, 'filters');
        getContent($scope.filtersIds, 'products');
    };

    $scope.isFilterChecked = function (filterId) {
        return !!$scope.filtersIds.includes(filterId);
    }
});
