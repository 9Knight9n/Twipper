FROM node:16-alpine

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json /app
COPY package-lock.json /app
RUN npm ci --silent
RUN npm install react-scripts@4.0.0 -g --silent
RUN npm install -g serve


# add app
COPY . /app

RUN npm run build

# start app
#CMD ["serve", "-s", "build"]
