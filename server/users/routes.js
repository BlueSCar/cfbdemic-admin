const userController = require('./controller');

module.exports = (app, auth) => {
    const controller = userController();

    app.route('/api/me').get(auth, controller.userInfo);
};
