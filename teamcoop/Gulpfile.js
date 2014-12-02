var gulp = require('gulp');
var mainBowerFiles = require('main-bower-files');
var less = require('gulp-less');
var jshint = require('gulp-jshint');
var livereload = require('gulp-livereload');
var minifyCSS = require('gulp-minify-css');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');
var connect = require('connect');
var del = require('del');
//var imagemin = require('gulp-imagemin');
var swig = require('gulp-swig');

// Edit this values to best suit your app
var WEB_PORT = 8000;
var APP_DIR = 'static';


var paths = {
    font: 'src/fonts/**/*.*',
    scripts: 'src/**/*.js',
    images: 'src/images/**/*',
    styles: 'src/css/**/*.less',
    tpl: 'templates/**/*.html'
};

// var opts = {
//     defaults: {
//         cache: false,
//         locals: {
//             site_name: "booksshelf"
//         }
//     },
//     data: {
//         headline: "Welcome"
//     }
// };

// bower
gulp.task('bower', function () {
    gulp.src(mainBowerFiles())
        .pipe(gulp.dest(APP_DIR + '/vendor'))
});

// jshint files

gulp.task('uglify', function () {
    gulp.src(paths.scripts)
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(APP_DIR));
});

// Copy all static images
gulp.task('images', function () {
    gulp.src(paths.images)
        .pipe(gulp.dest(APP_DIR + '/images'));
});
// fonts
gulp.task('fonts', function () {
    gulp.src(paths.font)
        .pipe(gulp.dest(APP_DIR + '/fonts'));
});

// Copy all static images and compress them
gulp.task('imagesmin', function () {
    gulp.src(paths.images)
        .pipe(imagemin({
            optimizationLevel: 3
        }))
        .pipe(gulp.dest(APP_DIR + '/images'));
});

gulp.task('less', function () {
    gulp.src('app/css/styles.less')
        .pipe(less())
        .pipe(minifyCSS())
        .pipe(gulp.dest(APP_DIR + '/stylesheets'));
});

// start local http server for development
gulp.task('http-server', function () {
    serveStatic = require('serve-static');
    connect()
        .use(require('connect-livereload')({
            port: 35729
        }))
        .use(serveStatic(APP_DIR))
        .listen(WEB_PORT);

    console.log('Server listening on http://localhost:' + WEB_PORT);
});


// start local http server with watch and livereload set up
gulp.task('server', function () {

    //gulp.run('lr-server');

    var watchFiles = [
            APP_DIR + '/*.html',
            APP_DIR + '/javascripts/*.js',
            APP_DIR + '/images/*',
            APP_DIR + '/stylesheets/styles.css',
    ];

    var server = livereload();
    gulp.watch(watchFiles).on('change', function (file) {
        server.changed(file.path);
    });

    gulp.run('http-server');
});

gulp.task('html', function () {
    gulp.src(paths.tpl)
        .pipe(swig({
            defaults: {
                cache: false,
                locals: {
                    site_name: "teamcoop"
                }
            }
        }))
        .pipe(gulp.dest(APP_DIR));
});

gulp.task('watch', function () {
    livereload.listen();
    gulp.watch(paths.styles, ['less']);
    gulp.watch(paths.scripts, ['uglify']);
    gulp.watch(paths.images, ['images']);
    gulp.watch(paths.tpl, ['html']);
    gulp.watch('app' + '/**').on('change', livereload.changed);
});

gulp.task('default', function () {
//    gulp.run('bower', 'less', 'uglify', 'images', 'fonts', 'watch', 'server', 'html');
    gulp.run('bower', 'less', 'uglify', 'fonts', 'watch');
});

gulp.task('dist', function () {
//    gulp.run('bower', 'less', 'uglify', 'images', 'fonts', 'html');
    gulp.run('bower', 'less', 'uglify', 'fonts');
});

gulp.task('clean', function (cb) {
    // You can use multiple globbing patterns as you would with `gulp.src`
    del([APP_DIR], cb);
    console.log('Files deleted');
});
