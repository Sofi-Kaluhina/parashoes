module.exports = function(grunt) {
    grunt.initConfig({



        includeSource: {
            options: {
                basePath: 'app',
                baseUrl: 'public/',
                templates: {
                    html: {
                        js: '<script src="{filePath}"></script>',
                        css: '<link rel="stylesheet" type="text/css" href="{filePath}" />',
                    },
                    haml: {
                        js: '%script{src: "{filePath}"}/',
                        css: '%link{href: "{filePath}", rel: "stylesheet"}/'
                    },
                    jade: {
                        js: 'script(src="{filePath}", type="text/javascript")',
                        css: 'link(href="{filePath}", rel="stylesheet", type="text/css")'
                    },
                    scss: {
                        scss: '@import "{filePath}";',
                        css: '@import "{filePath}";',
                    },
                    less: {
                        less: '@import "{filePath}";',
                        css: '@import "{filePath}";',
                    },
                        ts: {
                        ts: '/// <reference path="{filePath}" />'
                    }
                }
                },
                myTarget: {
                    files: {
                        'build/app.html': 'app.html'
                }
            }
        },

        jshint: {
            all: ['scripts/**/*.js']
        },

        concat: {
            dist: {
                src: [
                    'scripts/**/*.js'
                ],
                dest: 'build/production.js'
            }
        },

        uglify: {
            build: {
                src: 'build/production.js',
                dest: 'build/production.min.js'
            }
        },

        clean: {
            js: ['build/*.js', '!build/*.min.js']
        },

        watch: {
            options: {livereload:true},
            files: ['scripts/**/*.js']
        }
    });

    grunt.loadNpmTasks('grunt-include-source');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-less');

    grunt.registerTask('default', ['concat', 'uglify', 'clean']);
    grunt.registerTask('hint', ['jshint']);
    grunt.registerTask('dev', ['includeSource']);
};

