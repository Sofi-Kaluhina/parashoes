/**
 * Created by markel on 25.08.16.
 */

app.controller('ProductPageController', function ($rootScope, $http, $scope, $routeParams) {
        $scope.productPageProduct = [];
        $scope.imagesForGallery = [];

        var slug_name = $routeParams.slug_name;

        $http.get($rootScope.apiUrl + $rootScope.baseUrl + 'product/' + slug_name)
            .success(function (response) {
                    $scope.productPageProduct = response;
                    $scope.productPageProduct[0].images.forEach(function (element, index) {
                        $scope.imagesForGallery.push(
                            {
                                thumb: $rootScope.apiUrl + element['thumb_path'],
                                small: $rootScope.apiUrl + element['small_path'],
                                large: $rootScope.apiUrl + element['large_path']
                            }
                        )
                    });
                    if ($scope.imagesForGallery.length != 0) {
                        $scope.zoomModelGallery01 = $scope.imagesForGallery[0];
                    }
                }
            );

        $scope.setApproot = function (appRoot) {
            //only change when needed.
            if ($scope.approot && appRoot === $scope.approot) {
                return;
            }
            $scope.approot = appRoot;
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
            scrollZoom: false,
            zoomWindowWidth: 600,
            zoomWindowHeight: 600,
            easing: true,
            zoomWindowFadeIn: 500,
            zoomWindowFadeOut: 500,
            lensFadeIn: 100,
            lensFadeOut: 100,

            initial: 'small',

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
