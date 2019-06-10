module.exports = (passport, crypto) => ({
    authJwt: passport.authenticate('jwt', {
        session: false,
        successRedirect: '/',
        failureRedirect: '/'
    }),
    addTokenToCookie: (req, res) => {
        res.cookie('jwt', req.account ? req.account : req.user, {
            httpOnly: true,
            secure: process.env.NODE_ENV !== 'development',
            domain: process.env.JWT_DOMAIN,
            maxAge: 7 * 24 * 60 * 60 * 1000
        });
        res.redirect('/auth');
    }
});
