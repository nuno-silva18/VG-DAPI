
var mysql = require('mysql')
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '',
  database : 'vg_dapi'
});

exports.getGameByName = function(req, res) {
    connection.query("SELECT * FROM game WHERE match(name, description) AGAINST (? IN NATURAL LANGUAGE MODE)", [req.body.name], function (err, results) {
        if (err) 
            console.log(err);
        res.json(results);
    })
};
