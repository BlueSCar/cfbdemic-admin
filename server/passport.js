const redditStrategy = require('./strategies/reddit');
const jwtStrategy = require('./strategies/jwt');

module.exports = (passport, db) => {
    redditStrategy(passport, db);
    jwtStrategy(passport, db);
};
