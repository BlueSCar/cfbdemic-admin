const express = require('express');
const helmet = require('helmet');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const path = require('path');
const history = require('connect-history-api-fallback');

const authRoutes = require('./auth/routes');

module.exports = (db, passport, rabbit) => {
    const app = express();
    app.use(helmet());

    app.enable('trust proxy');
    app.use(cookieParser());

    app.use(bodyParser.json());
    app.use(bodyParser.urlencoded({
        extended: true
    }));

    app.use(passport.initialize());

    if (process.env.NODE_ENV === 'development') {
        app.use(cors());
    }

    // const auth = passport.authenticate('jwt', {
    //     session: false
    // });

    // routes
    authRoutes(app, passport);
    // routes(app, db, auth);

    app.use(history());

    app.use(express.static(path.join(__dirname, '../dist')));
    app.use('/css', express.static(path.join(__dirname, '../dist/css')));
    app.use('/img', express.static(path.join(__dirname, '../dist/img')));
    app.use('/js"', express.static(path.join(__dirname, '../dist/js')));

    app.get('/', (req, res) => {
        res.sendFile(path.join(__dirname + '/dist/index.html')); // eslint-disable-line
    });

    return app;
};
