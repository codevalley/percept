FROM node:14 as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Accept environment variables as build arguments
ARG VUE_APP_API_URL

# Create .env file or use an existing .env.production file
RUN echo "VUE_APP_API_URL=${VUE_APP_API_URL}" > .env.production

RUN npm run build

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY frontend-nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]