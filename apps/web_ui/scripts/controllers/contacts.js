/**
 * Created by markel on 16.08.16.
 */

app.controller('ContactsController', function ($scope) {

    $scope.initialize = (function () {
        $scope.myLatlng = new google.maps.LatLng(47.096030, 37.547198);
        $scope.myOptions = {
            zoom: 16,
            center: $scope.myLatlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            scrollwheel: false
        };
        $scope.map = new google.maps.Map(document.getElementById("map_canvas"), $scope.myOptions);

        $scope.marker = new google.maps.Marker({
            position: $scope.myLatlng,
            map: $scope.map,
            title: "Мы тут!"
        });

        $scope.contentString = '<div id="content">' +
            '<p style="font-weight: bold">' + '"ParaShoes"' + '</p>' +
            'пр. Мира, 62/37' +
            '<p>' + 'Пн-Вс с 9:00 до 19:00' + '</p>' +
            '<a target="_blank" href="https://maps.google.com/maps?ll=47.096030,37.547198&z=18&t=m&hl=ru-RU&gl=US&mapclient=apiv3&cid=15462233706182546960">' +
            '<p>' + ' Показать на Google Картах' + '</p>' +
            '</a>' +
            '</div>';

        $scope.infowindow = new google.maps.InfoWindow({
            content: $scope.contentString
        });
        google.maps.event.addListener($scope.marker, 'click', function () {
            $scope.infowindow.open($scope.map, $scope.marker);
        });

        $scope.myLatlng2 = new google.maps.LatLng(47.127851, 37.564193); /* 47.127851, 37.564193 */
        $scope.myOptions2 = {
            zoom: 16,
            center: $scope.myLatlng2,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            scrollwheel: false
        };
        $scope.map2 = new google.maps.Map(document.getElementById("map_canvas-2"), $scope.myOptions2);

        $scope.marker2 = new google.maps.Marker({
            position: $scope.myLatlng2,
            map: $scope.map2,
            title: "Мы тут!"
        });

        $scope.contentString2 = '<div id="content2">' +
            '<p style="font-weight: bold">' + '"ParaShoes"' + '</p>' +
            'пр. Металлургов, 164' +
            '<p>' + 'Пн-Вс с 9:00 до 19:00' + '</p>' +
            '<a target="_blank" href="https://maps.google.com/maps/place/Медиа-поиск/' +
            '@47.127851,37.564193,17z/data=!4m13!1m7!3m6!1s0x0:0x0!2zNDfCsDA1JzUwLjYiTiAzN8KwMzInNTkuNyJF!3b1!8m2!3d' +
            '47.127851!4d37.564193!3m4!1s0x0:0x7edc8b93cd2c7f4!8m2!3d47.0970338!4d37.5497621">' +
            '<p>' + ' Показать на Google Картах' + '</p>' +
            '</a>' +
            '</div>';

        $scope.infowindow2 = new google.maps.InfoWindow({
            content: $scope.contentString2
        });
        google.maps.event.addListener($scope.marker2, 'click', function () {
            $scope.infowindow2.open($scope.map2, $scope.marker2);
        });
    })();
});