FROM node:19.5.0-alpine

COPY ./nextjs-blog /nextjs-blog

WORKDIR /nextjs-blog

COPY package*.json ./

RUN npm install

ENTRYPOINT ["entrypoint.sh"]
# CMD ["npm", "run", "dev"]