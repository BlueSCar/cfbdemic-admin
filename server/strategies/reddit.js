const RedditStrategy = require('passport-reddit').Strategy;
const jwt = require('jsonwebtoken');

module.exports = (passport, db) => {
    const appId = process.env.REDDIT_ID;
    const appSecret = process.env.REDDIT_SECRET;
    const webHost = process.env.WEB_HOST;

    passport.use(new RedditStrategy({
        clientID: appId,
        clientSecret: appSecret,
        callbackURL: `http://${webHost}/auth/reddit/callback`,
        passReqToCallback: true
    }, (req, accessToken, refreshToken, profile, done) => {
        process.nextTick(async () => {
            try {
                let user = null;

                if (!req.user) {
                    const result = await db.oneOrNone(
                        'SELECT * FROM player WHERE name = $1', [
                            profile.name
                        ]
                    );

                    if (!result) {
                        const id = await db.one(
                            'INSERT INTO player (name) VALUES ($1) RETURNING id',
                            [profile.name]
                        );

                        user = {
                            id: id.id,
                            name: profile.name
                        };
                    } else {
                        user = {
                            id: result.id,
                            name: result.name
                        };
                    }
                } else {
                    user = {
                        id: req.user.id,
                        name: req.user.name
                    };
                }

                const token = jwt.sign(user, process.env.JWT_SECRET, {
                    issuer: 'CFBDemic Allies',
                    subject: user.name,
                    audience: process.env.JWT_DOMAIN
                });

                return done(null, token);
            } catch (err) {
                return done(err, null);
            }
        });
    }));
};
