/**
 * Created by sofi on 24.12.16.
 */
app.controller('FeedbackController', function ($scope, $http) {
    $scope.user = '';
    $scope.email = '';
    $scope.myTextarea = '';
    $scope.submit = function () {
        alert('Сообщение отправлено');
        $scope.user = null;
        $scope.email = null;
        $scope.myTextarea = null;
        $scope.myForm.$setUntouched();
        $scope.myForm.$setPristine();
    }
});