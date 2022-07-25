FROM node:18.6-alpine

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json /app
COPY package-lock.json /app
RUN npm cache verify
RUN npm install


# add app
COPY . /app

# start app
# CMD ["npm", "start"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]