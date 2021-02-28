FROM node:15-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./

COPY yarn.lock ./

RUN yarn install --silent

COPY . ./

CMD ["yarn", "start"]
