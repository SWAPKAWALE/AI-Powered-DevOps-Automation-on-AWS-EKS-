# Frontend Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install --production=false --legacy-peer-deps --workspaces=false \
    && npm install ajv@8 ajv-keywords@5 --legacy-peer-deps --workspaces=false

COPY . .

RUN CI=false npm run build

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000", "--single"]
