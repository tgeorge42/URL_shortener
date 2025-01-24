# Étape 1 : Construire le frontend
FROM node:18 as build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Étape 2 : Démarrer l'application frontend
FROM node:18

WORKDIR /app

COPY --from=build /app /app

CMD ["npm", "run", "dev"]
