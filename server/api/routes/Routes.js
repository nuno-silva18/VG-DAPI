'use strict';
module.exports = function(app) {
  var controller = require('../controllers/Controller');
      // todoList Routes
  app.route('/game/name')
    .post(controller.getGameByName)
};