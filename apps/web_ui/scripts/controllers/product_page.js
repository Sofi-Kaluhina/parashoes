/**
 * Created by markel on 25.08.16.
 */

app.controller('ProductPageController', function ($rootScope, $http, $scope, $routeParams) {
        $scope.product = [];
        $scope.imagesForGallery = [];

        var current_id = $routeParams.id;

        $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'product/' + current_id)
            .success(function (responce) {
                    $scope.product = responce;
                    $scope.product[0].images.forEach(function (element, index) {
                        $scope.imagesForGallery.push(
                            {
                                thumb: $rootScope.apiUrl + element['thumb_path'],
                                small: $rootScope.apiUrl + element['thumb_path'],
                                large: $rootScope.apiUrl + element['path']
                            }
                        )
                    });
                }
            );

        $scope.setApproot = function (appRoot) {
            //only change when needed.
            if ($scope.approot && appRoot === $scope.approot) {
                return;
            }
            $scope.approot = appRoot;

            // $scope.zoomModel1 = $scope.imagesForGallery[0];
            // $scope.zoomModel2 = $scope.imagesForGallery[1];

            $scope.zoomModelGallery01 = $scope.imagesForGallery[0];
            // $scope.zoomModelGallery04 = $scope.imagesForGallery[3];
            // $scope.zoomModelGallery05 = $scope.imagesForGallery[0];

            $scope.colorboxWithCallbacks = {
                opacity: 0.5,
                open: false,
                href: appRoot + 'images/large/image1.jpg',
                onOpen: function () {
                    alert('on open');
                },
                onClosed: function () {
                    alert('on closed');
                },
                onLoad: function () {
                    alert('on load');
                },
                onComplete: function () {
                    alert('on complete');
                },
                onCleanup: function () {
                    alert('on cleanup');
                }
            };
        };

        //default
        $scope.setApproot('');

        $scope.zoomOptions = {
            scrollZoom: true,
            zoomWindowWidth: 600,
            zoomWindowHeight: 600,
            easing: true,
            zoomWindowFadeIn: 500,
            zoomWindowFadeOut: 500,
            lensFadeIn: 500,
            lensFadeOut: 500,

            initial: 'small'
        };

        $scope.zoomOptionsGallery01 = {
            scrollZoom: true,
            zoomWindowWidth: 600,
            zoomWindowHeight: 600,
            easing: true,
            zoomWindowFadeIn: 500,
            zoomWindowFadeOut: 500,
            lensFadeIn: 500,
            lensFadeOut: 500,

            initial: 'large',

            gallery: 'gallery_01',
            cursor: 'pointer',
            galleryActiveClass: "active",
            imageCrossfade: true,
            loadingIcon: false
        };

        $scope.setActiveImageInGallery = function (prop, img) {
            $scope[prop] = img;
            //console.log(img);
        };
        $scope.setScopeValue = function (prop, value) {
            $scope[prop] = value;
        };

    });
