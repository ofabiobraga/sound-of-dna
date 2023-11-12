FROM node:20.7.0

WORKDIR /app/ui

COPY package.json /app/ui
COPY package-lock.json /app/ui

RUN npm install

COPY . /app/ui

CMD ["npm", "run", "dev"]