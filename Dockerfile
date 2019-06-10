FROM node:10-alpine

RUN mkdir -p /home/node/app/node_modules && mkdir -p /home/node/app/dist && chown -R node:node /home/node/app

WORKDIR /home/node/app

COPY package*.json ./

RUN npm install pm2 -g
RUN npm install

RUN npm run build

COPY . .
COPY --chown=node:node . .

USER node

EXPOSE 8080

CMD [ "pm2-runtime", "index.js" ]
