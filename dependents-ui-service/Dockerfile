FROM node:10 AS build
COPY . /opt/dependents/
WORKDIR /opt/dependents/
RUN npm install
RUN npm run build

FROM nginx
COPY --from=build /opt/dependents/dist /usr/share/nginx/html