const jwtStrategy = require('./strategies/jwt');

module.exports = (passport, db) => {
    jwtStrategy(passport, db);
};
