/**
 * Created by markel on 04.12.16.
 */
app.controller('UserListController', function ($rootScope, $http, $scope, $uibModal, $log) {

    $scope.animationsEnabled = true;

    $scope.getUserList = function() {
        $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'admin/user/list')
            .then(function (response) {
                    $scope.userList = response.data
                }
            );
        };

    $scope.getUserList();

    $scope.openUserDeletePopup = function (userId) {
        var modalInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/template/user/modal/delete.html',
            controller: 'UserDeleteInstanceController',
            controllerAs: '$scope'
        });

        modalInstance.result.then(function () {
            $http({
                method: 'DELETE',
                url: $rootScope.apiUrl + $rootScope.baseUrl + 'admin/user/list?user_id=' + userId,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json'
                }
            }).then(
                function (response) {
                    $scope.getUserList();
                    $log.info(response.statusText + ' at: ' + new Date());
                },
                function (response) {
                    $log.info(response.statusText + ' at: ' + new Date());
                    $scope.getUserList();
                }
            );
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
            $scope.getUserList();
        });
    };

    $scope.openUserEditPopup = function (userId) {
        var modalInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/template/user/modal/edit.html',
            controller: 'UserEditInstanceController',
            controllerAs: '$scope',
            scope: $scope,
            resolve: {
                userEditDetails: function () {
                    return $scope.userList[userId - 1]
                }
            }
        });

        modalInstance.result.then(function (userEditDetails) {
            $log.info(userEditDetails);
            $scope.getUserList();
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.openUserAddPopup = function () {
        var modalInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/template/user/modal/add.html',
            controller: 'UserAddInstanceController',
            controllerAs: '$scope',
            scope: $scope
        });

        modalInstance.result.then(function (userAddDetails) {
            $log.info(userAddDetails);
            $http({
                method: 'POST',
                url: $rootScope.apiUrl + $rootScope.baseUrl + 'admin/user/list',
                data: userAddDetails,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json'
                }
            }).then( function (response) {
                    $log.info(response.statusText + ' at: ' + new Date());
                    $scope.getUserList();
                }
            );
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
            $scope.getUserList();
        });
    };

    $scope.toggleAnimation = function () {
        $scope.animationsEnabled = !$scope.animationsEnabled;
    };

});

app.controller('UserDeleteInstanceController', function ($scope, $uibModalInstance) {
    $scope.ok = function () {
        $uibModalInstance.close();
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});

app.controller('UserEditInstanceController', function ($scope, $uibModalInstance) {
    $scope.ok = function () {
        $uibModalInstance.close($scope.userEdit);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});

app.controller('UserAddInstanceController', function ($scope, $uibModalInstance) {
    $scope.ok = function () {
        $uibModalInstance.close($scope.userAdd);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});
