/**
 * Created by sofi on 24.12.16.
 */
app.controller('FeedbackController', function ($rootScope, $scope, $http, $location, $log, FeedbackFactory) {

    /* Making textarea's height equal to text's height */
    $('textarea').keyup(function () {
        $(this).height(100);
        $(this).height(this.scrollHeight);
    });
    $scope.submit = function () {
        $http({
            method: 'POST',
            url: $rootScope.apiUrl + $rootScope.baseUrl + 'feedback/post',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            },
            data: {
                username: $scope.username,
                email: $scope.email,
                message: $scope.message
            }
        }).then(
            function (response) {
                /* Clean data object */
                // $scope.data = {};

                /* Cleaning form */
                $scope.username = null;
                $scope.email = null;
                $scope.message = null;
                $scope.myForm.$setUntouched();
                $scope.myForm.$setPristine();

                FeedbackFactory.setData(
                    'сообщение успешно отправлено',
                    response.data.message
                );

                /* Relocation when success */
                $location.path('/feedback/thanx');
            }, function () {
                FeedbackFactory.setData(
                    'сообщение не отправлено',
                    'Не в этот раз, сервер лежит!'
                );
            }
        );
    };
    $scope.thanx = FeedbackFactory.getData();
});

app.factory('FeedbackFactory', function () {
    var result = {
        status: "",
        message: ""
    };
    return {
        setData: function (status, message) {
            result = {
                status: status,
                message: message
            };
        },
        getData: function () {
            return result;
        }
    }
});

// url для отправки запроса
// feedback/post
// Параметры:
// username - text
// email - text
// message - text


// По образу и подобию:


// $scope.data = {
//     username: $scope.username,
//     email: $scope.email,
//     message: $scope.message
// };