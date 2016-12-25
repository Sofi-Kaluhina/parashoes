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
                }
            );
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
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

        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
            $log.info($scope.userEdit);
            $scope.getUserList();
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.toggleAnimation = function () {
        $scope.animationsEnabled = !$scope.animationsEnabled;
    };

});

app.controller('UserEditInstanceController', function ($scope, $uibModalInstance, userEditDetails) {
    $scope.userEditDetails = userEditDetails;

    $scope.modUserEditDetails = function () {
        $scope.userEditDetails.login = $scope.userEdit.login;
        // firstname: $scope.userEditDetails.firstname,
        // lastname: $scope.userEditDetails.lastname,
        // gender: $scope.userEditDetails.gender,
        // email: $scope.userEditDetails.email,
        // created_at: $scope.userEditDetails.created_at,
        // last_login_at: $scope.userEditDetails.last_login_at
    };

    $scope.ok = function () {
        $uibModalInstance.close($scope.selected);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
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
