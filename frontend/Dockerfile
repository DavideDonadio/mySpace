FROM node:22-alpine

WORKDIR /app

# Install dependencies leveraging Docker layer caching
COPY package*.json ./
RUN npm install

# Copy application source code
COPY . .

EXPOSE 4321

ENV HOST=0.0.0.0
ENV PORT=4321

CMD ["npm", "run", "dev", "--", "--host"]
