
/**
 * Module dependencies.
 */

var express = require('express');
var routes = require('./routes');

var app = module.exports = express.createServer();
var io = require('socket.io')(app);

var zmq = require('zmq');
var zmq_publisher = zmq.socket('pub');

zmq_publisher.bindSync("tcp://127.0.0.1:45321");

// Configuration

app.configure(function(){
  app.set('views', __dirname + '/views');
  app.set('view engine', 'ejs');
  app.use(express.bodyParser());
  app.use(express.methodOverride());
app.use(express.compiler({ src : __dirname + '/public', enable: ['less']}));
  app.use(app.router);
  app.use(express.static(__dirname + '/public'));
});

app.configure('development', function(){
  app.use(express.errorHandler({ dumpExceptions: true, showStack: true }));
});

app.configure('production', function(){
  app.use(express.errorHandler());
});

// Compatible

// Now less files with @import 'whatever.less' will work(https://github.com/senchalabs/connect/pull/174)
var TWITTER_BOOTSTRAP_PATH = './vendor/twitter/bootstrap/less';
express.compiler.compilers.less.compile = function(str, fn){
  try {
    var less = require('less');var parser = new less.Parser({paths: [TWITTER_BOOTSTRAP_PATH]});
    parser.parse(str, function(err, root){fn(err, root.toCSS());});
  } catch (err) {fn(err);}
};

// Routes

app.get('/', routes.index);

app.listen(1234, function(){
  console.log("Express server listening on port %d in %s mode", app.address().port, app.settings.env);
});

var themes = [
  "calm",
  "mellow",
  "study",
  "movie1",
  "movie2",
  "party",
  "seizure1",
  "seizure2",
];


function isValidStrip(strip) {
  return strip == "l" || strip == "rl" || strip == "r";
}

function isValidPasscode(passcode) {
  return true;
}

function isValidColor(color) {
  var colorTester = /^#[0-9a-f]{6}$/;
  return colorTester.test(color);
}

function isValidTheme(theme) {
  for (var i in themes) {
    if (theme == themes[i]) {
      return true;
    }
  }
  return false;
}

io.on('connection', function (socket) {
  socket.on('color', function (data) {
    color = data['color'];
    passcode = data['passcode'];
    strip = data['strip'];
    if (isValidColor(color) && isValidPasscode(passcode) && isValidStrip(strip)) {
      update = {type: 'color', strip: strip, color: color};
      zmq_publisher.send(JSON.stringify(update));
    }
  });
  socket.on('theme', function (data) {
    theme = data['theme'];
    passcode = data['passcode'];
    strip = data['strip'];
    if (isValidTheme(theme) && isValidPasscode(passcode) && isValidStrip(strip)) {
      update = {type: 'theme', strip: strip, theme: theme};
      zmq_publisher.send(JSON.stringify(update));
    }
  });
});
