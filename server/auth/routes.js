const crypto = require('crypto');
const authController = require('./controller');

module.exports = (app, passport) => {
    const controller = authController(passport, crypto);

    app.route('/auth').get(controller.authJwt);
};
