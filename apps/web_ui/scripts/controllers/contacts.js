/**
 * Created by markel on 16.08.16.
 */

app.controller('ContactsController', function($scope) {

    $scope.initialize = (function () {
        $scope.myLatlng = new google.maps.LatLng(47.100035, 37.553630);
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
            title:"Мы тут!"
        });

        $scope.contentString = '<div id="content">' +
            '<p style="font-weight: bold">' + '"BUlavka"' + '</p>' +
            'ул. Артема, 59' +
            '<p>' + 'Пн-Вс с 9:00 до 19:00' + '</p>' +
            '<a target="_blank" href="https://maps.google.com/maps?ll=47.100236,37.553397&z=18&t=m&hl=ru-RU&gl=US&mapclient=apiv3&cid=15462233706182546960">' +
            '<p>' + ' Показать на Google Картах'+ '</p>' +
            '</a>' +
            '</div>';

        $scope.infowindow = new google.maps.InfoWindow({
            content: $scope.contentString
        });
        google.maps.event.addListener($scope.marker, 'click', function() {
            $scope.infowindow.open($scope.map,$scope.marker);
        });
    })();
});