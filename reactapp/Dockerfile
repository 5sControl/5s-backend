FROM node:17-alpine
WORKDIR /build
COPY package.json /app/package.json
RUN npm install --only=prod
COPY . /app
RUN npm run build