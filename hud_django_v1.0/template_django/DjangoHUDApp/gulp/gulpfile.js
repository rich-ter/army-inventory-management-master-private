var gulp        = require('gulp');
var sass        = require('gulp-sass')(require('sass'));
var minifyCSS   = require('gulp-clean-css');
var concat      = require('gulp-concat');
var sourcemaps  = require('gulp-sourcemaps');
var livereload  = require('gulp-livereload');
var connect     = require('gulp-connect');
var header      = require('gulp-header');
var uglify      = require('gulp-uglify');
var rename      = require('gulp-rename');
var fileinclude = require('gulp-file-include');
var autoprefixer = require('gulp-autoprefixer');

gulp.task('css-vendor', function(){
	return gulp.src([
			'node_modules/@fortawesome/fontawesome-free/css/all.min.css',
			'node_modules/bootstrap-icons/font/bootstrap-icons.css',
			'node_modules/jquery-ui-dist/jquery-ui.min.css',
			'node_modules/animate.css/animate.min.css',
			'node_modules/pace-js/themes/black/pace-theme-flash.css',
			'node_modules/perfect-scrollbar/css/perfect-scrollbar.css'
		])
		.pipe(sass())
		.pipe(concat('vendor.min.css'))
		.pipe(minifyCSS())
		.pipe(gulp.dest('../static/css/'))
		.pipe(livereload());
});

gulp.task('css-app', function(){
  return gulp.src([
			'src/scss/font.scss',
			'src/scss/styles.scss'
		])
		.pipe(sass())
		.pipe(concat('app.min.css'))
    .pipe(autoprefixer())
		.pipe(minifyCSS())
		.pipe(gulp.dest('../static/css/'))
		.pipe(livereload());
});

gulp.task('css-img', function(){
	return gulp.src([ 'src/scss/images/**' ])
		.pipe(gulp.dest('../static/css/images'));
});

gulp.task('fonts', function() {
	gulp.src(['node_modules/bootstrap-icons/font/fonts/*'])
		.pipe(gulp.dest('../static/css/fonts/'));
	return gulp.src(['node_modules/@fortawesome/fontawesome-free/webfonts/*'])
		.pipe(gulp.dest('../static/webfonts/'));
});

gulp.task('img', function() {
	return gulp.src(['src/img/**'])
		.pipe(gulp.dest('../static/img/'))
		.pipe(livereload());
});

gulp.task('plugins', function() {
	var pluginFiles = [
		'node_modules/@fortawesome/**',
		'node_modules/@fullcalendar/**',
		'node_modules/@highlightjs/cdn-assets/**',
		'node_modules/animate.css/**',
		'node_modules/apexcharts/**',
		'node_modules/bootstrap/**',
		'node_modules/bootstrap-icons/**',
		'node_modules/blueimp-file-upload/**',
		'node_modules/blueimp-tmpl/**',
		'node_modules/blueimp-gallery/**',
		'node_modules/blueimp-canvas-to-blob/**',
		'node_modules/blueimp-load-image/**',
		'node_modules/bootstrap-datepicker/**',
		'node_modules/bootstrap-daterangepicker/**',
		'node_modules/bootstrap-slider/**',
		'node_modules/bootstrap-timepicker/**',
		'node_modules/bootstrap-table/**',
		'node_modules/chart.js/**',
		'node_modules/datatables.net/**',
		'node_modules/datatables.net-bs5/**',
		'node_modules/datatables.net-autofill/**',
		'node_modules/datatables.net-autofill-bs5/**',
		'node_modules/datatables.net-buttons/**',
		'node_modules/datatables.net-buttons-bs5/**',
		'node_modules/datatables.net-colreorder/**',
		'node_modules/datatables.net-colreorder-bs5/**',
		'node_modules/datatables.net-fixedcolumns/**',
		'node_modules/datatables.net-fixedcolumns-bs5/**',
		'node_modules/datatables.net-fixedheader/**',
		'node_modules/datatables.net-fixedheader-bs5/**',
		'node_modules/datatables.net-keytable/**',
		'node_modules/datatables.net-keytable-bs5/**',
		'node_modules/datatables.net-responsive/**',
		'node_modules/datatables.net-responsive-bs5/**',
		'node_modules/datatables.net-rowgroup/**',
		'node_modules/datatables.net-rowgroup-bs5/**',
		'node_modules/datatables.net-rowreorder-bs5/**',
		'node_modules/datatables.net-scroller/**',
		'node_modules/datatables.net-scroller-bs5/**',
		'node_modules/datatables.net-select/**',
		'node_modules/datatables.net-select-bs5/**',
		'node_modules/jquery/**',
		'node_modules/jquery-migrate/**',
		'node_modules/jquery-typeahead/**',
		'node_modules/jquery-ui-dist/**',
		'node_modules/jquery.maskedinput/**',
		'node_modules/js-cookie/**',
		'node_modules/jszip/**',
		'node_modules/jvectormap-content/**',
		'node_modules/jvectormap-next/**',
		'node_modules/kbw-countdown/**',
		'node_modules/lity/**',
		'node_modules/masonry-layout/**',
		'node_modules/moment/**',
		'node_modules/pace-js/**',
		'node_modules/pdfmake/**',
		'node_modules/perfect-scrollbar/**',
		'node_modules/photoswipe/**',
		'node_modules/select-picker/**',
		'node_modules/spectrum-colorpicker2/**',
		'node_modules/summernote/**',
		'node_modules/tag-it/**'
	];
	return gulp.src(pluginFiles, { base: './node_modules/' }).pipe(gulp.dest('../static/plugins'));
});

gulp.task('js-vendor', function(){
  return gulp.src([
			'node_modules/pace-js/pace.min.js',
			'node_modules/jquery/dist/jquery.min.js',
			'node_modules/jquery-ui-dist/jquery-ui.min.js',
			'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js',
			'node_modules/perfect-scrollbar/dist/perfect-scrollbar.min.js',
			'node_modules/js-cookie/dist/js.cookie.min.js'
		])
		.pipe(sourcemaps.init())
		.pipe(concat('vendor.min.js'))
		.pipe(sourcemaps.write())
		.pipe(gulp.dest('../static/js'))
		.pipe(livereload())
});

gulp.task('js-app', function(){
	return gulp.src([
			'src/js/app.js',
		])
		.pipe(uglify())
    .pipe(rename('app.min.js'))  
		.pipe(gulp.dest('../static/js'))
		.pipe(livereload())
});

gulp.task('js-demo', function(){
	return gulp.src('src/js/demo/*')
		.pipe(gulp.dest('../static/js/demo/'))
		.pipe(livereload());
});

gulp.task('watch', function () {
	livereload.listen();
	gulp.watch('src/scss/*.scss', gulp.series(gulp.parallel(['css-app'])));
	gulp.watch('src/scss/*/*.scss', gulp.series(gulp.parallel(['css-app'])));

	gulp.watch('src/js/*.js', gulp.series(gulp.parallel(['js-app'])));
	gulp.watch('src/js/*/*.demo.js', gulp.series(gulp.parallel(['js-demo'])));

	gulp.watch('src/img/*', gulp.series(gulp.parallel(['img'])));
});

gulp.task('default', gulp.series(gulp.parallel([
	'css-vendor', 
	'css-app', 
	'css-img', 
	'js-vendor', 
	'js-app', 
	'js-demo', 
	'img',
	'fonts', 
	'watch'
])));