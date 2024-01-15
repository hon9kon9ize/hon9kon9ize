ARG NODE_VERSION=20.11.0

# Alpine image
FROM node:${NODE_VERSION}-alpine AS alpine
RUN apk update
RUN apk add --no-cache libc6-compat
RUN apk add --no-cache yarn

FROM alpine as builder
WORKDIR  /app
RUN yarn global add turbo
COPY . .
RUN turbo prune --scope=@hon9kon9ize/extension-api --docker

# Prune projects
FROM alpine AS installer
RUN apk update
WORKDIR  /app
COPY --from=builder /app/out/json/ .
COPY --from=builder /app/out/yarn.lock .yarn.lock
COPY --from=builder /app/turbo.json ./turbo.json
RUN yarn install --frozen-lockfile

FROM alpine AS sourcer
WORKDIR /app
COPY --from=installer /app/ .
COPY --from=builder /app/out/full/ .
COPY .gitignore .gitignore
RUN yarn turbo run build --scope=@hon9kon9ize/extension-api --include-dependencies --no-deps

FROM alpine as runner
WORKDIR /app
COPY --from=sourcer /app/ .
CMD [ "node", "apps/extension-api/dist/index.js" ]