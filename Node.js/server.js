var express= require('express');
var app=express();
var server=require('http').createServer(app);
var io=require('socket.io').listen(server);

users=[]; //for user
connections=[] //for connections


server.listen(3000);
console.log('Server running......');


app.get('/',function(req, res) {

	res.sendFile(__dirname + '/index.html');

});

//open connection with a socket .io

io.on('connection', function (socket) {
  socket.emit('news', { hello: 'world' });
  socket.on('my other event', function (data) {
    console.log(data);
  });
});