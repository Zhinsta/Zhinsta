var gulp = require('gulp');
var less = require('gulp-less');
var uglify = require('gulp-uglify');
var path = require('path');

gulp.task('default', function() {
    gulp.src('./css/**/g.less')
        .pipe(less({
          paths: [ path.join(__dirname, 'css') ]
        }))
        .pipe(gulp.dest('../zhinsta/static/css'));

    gulp.src('./js/*.js')
        .pipe(uglify())
        .pipe(gulp.dest('../zhinsta/static/js'));

    gulp.src('./assets/imgs/*')
        .pipe(gulp.dest('../zhinsta/static/assets/imgs'));
});
