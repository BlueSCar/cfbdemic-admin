const amqp = require('amqplib');
const bluebird = require('bluebird');
const dotenv = require('dotenv');
const passport = require('passport');
const pgp = require('pg-promise');

const dbConfig = require('./server/database');
const expressConfig = require('./server/express');
const passportConfig = require('./server/passport');
const rabbitConfig = require('./server/rabbit');
const consumerConfig = require('./server/consumers');

(async () => {
    dotenv.config();

    const port = process.env.SERVER_PORT;

    const db = dbConfig(bluebird, pgp);
    const rabbit = await rabbitConfig(amqp);
    passportConfig(passport, db);
    const app = expressConfig(db, passport);

    await consumerConfig(rabbit.channel);

    app.listen(port, console.log(`Listening on port ${port}`));
})().catch((err) => {
    console.error(err);
});
