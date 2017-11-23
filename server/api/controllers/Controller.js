
let mysql = require('mysql');
let howlongtobeat = require("howlongtobeat");
let hltbService = new howlongtobeat.HowLongToBeatService();
let Bottleneck = require("bottleneck");
let limiter = new Bottleneck(10, 1000, -1, Bottleneck.strategy.LEAK, false);

let connection = mysql.createConnection({
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

// query fulltext games on steam with metacritic score and steam score > 90
// query best games in a genre sorted by metacritic
// query games that take less than 20 hours to beat sorted by score
// query games that cost less than 30 USD and take less than 20 hours to beat
let hltb_handler = function(result,name){
    let hltb_main=null;
    let hltb_complete=null;
    for(let i=0;i<result.length;i++){
        if(result[i].similarity>0.8){
            if(result[i].gameplayMain>0)
                hltb_main=result[i].gameplayMain;
            if(result[i].gameplayCompletionist>0)
                hltb_complete=result[i].gameplayCompletionist;
            connection.query("UPDATE Game SET HLTB_Main=?,HLTB_Complete=? WHERE name=?",[hltb_main,hltb_complete,name], function (err, results) {
                if (err) 
                    console.log(err);
                console.log("changed "+name);
            }) 
        }
    }
    
}
let hltb_promise = function(name){
    return hltbService.search(name).then(result =>hltb_handler(result,name));
}
exports.getHLTBAll = function(req, res){
  
    connection.query("SELECT name FROM Game", function (err, results) {
        if (err) 
            console.log(err);
        for(let i=0;i<results.length;i++){  
            limiter.schedule(hltb_promise,results[i].name);
        }
     })
};


