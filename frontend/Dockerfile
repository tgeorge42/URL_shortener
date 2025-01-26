# Frontend build
FROM node:20 as build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Start the frontend
FROM node:20

WORKDIR /app

COPY --from=build /app /app

CMD ["npm", "run", "dev"]
