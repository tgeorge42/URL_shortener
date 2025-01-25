# Étape 1 : Construire le frontend
FROM node:20 as build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Étape 2 : Démarrer l'application frontend
FROM node:20

WORKDIR /app

COPY --from=build /app /app

CMD ["npm", "run", "dev"]
