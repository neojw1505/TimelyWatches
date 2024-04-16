FROM node:21-alpine

# Install xdg-utils
RUN apk add --no-cache xdg-utils

WORKDIR /app

COPY package.json .

RUN npm install --force

COPY . .

RUN rm -rf node_modules/.cache node_modules/.vite

EXPOSE 3000

CMD ["npm", "run", "dev"]