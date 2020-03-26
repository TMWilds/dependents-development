FROM node:10
COPY . /opt/dependents/
WORKDIR /opt/dependents/
RUN npm install
RUN npm run build

FROM nginx
COPY /opt/dependents/dist /usr/share/nginx/html