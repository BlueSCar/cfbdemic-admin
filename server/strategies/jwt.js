const JWTStrategy = require('passport-jwt').Strategy;

const cookieExtractor = (req) => { // eslint-disable-line
    return req && req.cookies ? req.cookies['jwt'] : null; // eslint-disable-line
};

module.exports = (passport) => {
    passport.use(new JWTStrategy({
        secretOrKey: process.env.JWT_SECRET,
        issuer: 'CFBDemic Allies',
        jwtFromRequest: cookieExtractor,
        passReqToCallback: true
    }, async (req, payload, done) => {
        try {
            done(null, {
                iat: payload.iat,
                id: payload.id,
                name: payload.name
            });
        } catch (err) {
            done(err, null);
        }
    }));
};
