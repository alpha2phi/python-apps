FROM node:15-alpine

# RUN npm install -g npm@latest

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./

COPY yarn.lock ./

RUN yarn install --silent

COPY . ./

CMD ["yarn", "start"]
