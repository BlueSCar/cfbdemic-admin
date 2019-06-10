const crypto = require('crypto');
const authController = require('./controller');

module.exports = (app, passport) => {
    const controller = authController(passport, crypto);

    app.route('/auth').get(controller.authJwt);
    app.route('/auth/reddit').get(controller.authReddit);
    app.route('/auth/reddit/callback').get(controller.authRedditCallback, controller.addTokenToCookie);
};
