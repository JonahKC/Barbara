/*
// Express App
const path = require('path');
const express = require('express');
const app = express();
const static = path.join(__dirname, 'static');
const PORT = process.env.PORT || 3000
const HOST =  process.env.HOST || "localhost";

app.use(express.static(static));

var server = app.listen(PORT, function () {
    console.log('listening on http://'+HOST+':'+PORT+'/');
});