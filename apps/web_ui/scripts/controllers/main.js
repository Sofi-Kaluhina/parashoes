/**
 * Created by sofi on 15.07.16.
 */

app.controller('MainController', function ($rootScope, $http, $scope, InitialData) {
    $scope.Products = [];
    $scope.currentPage = 1; // keeps track of the current page
    $scope.pageSize = 10; // holds the number of items per page


    $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'products')
        .success(function (response) {
                $scope.Products = response;
            }
        );

    InitialData.async().then(function(responce) {
        $scope.initialData = responce;
    });

    /* JQuery for scroll-on-top button */

    $(document).ready(function() {
        $(window).scroll(function() {
            if($(this).scrollTop() > 100){
                $('#goTop').stop().animate({
                    top: '320px'
                }, 500);
            }
            else{
                $('#goTop').stop().animate({
                    top: '-100px'
                }, 500);
            }
        });
        $('#goTop').click(function() {
            $('html, body').stop().animate({
                scrollTop: 0
            }, 500, function() {
                $('#goTop').stop().animate({
                    top: '-100px'
                }, 500);
            });
        });
    });
});

app.filter('start', function () {
    return function (input, start) {
        if (!input || !input.length) {
            return;
        }
        start = +start;
        return input.slice(start);
    };
});
