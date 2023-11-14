FROM node:20.7.0

WORKDIR /app/ui

COPY package.json ./package.json
COPY package-lock.json ./package-lock.json

RUN npm i install

ENV PATH ./node_modules/.bin:$PATH

COPY . .

CMD ["npm", "run", "dev"]