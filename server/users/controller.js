module.exports = () => ({
    userInfo: async (req, res) => {
        if (req.isAuthenticated() && req.user) {
            res.send({
                id: req.user.id,
                name: req.user.name
            });
        } else {
            res.sendStatus(404);
        }
    }
});
