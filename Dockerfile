# Etapa build
FROM golang:1.20-alpine AS builder
RUN apk add --no-cache git
WORKDIR /app
RUN go install github.com/pocketbase/pocketbase@latest
WORKDIR /root/go/bin
RUN pocketbase build

# Etapa runtime
FROM alpine:latest
RUN apk add --no-cache ca-certificates
WORKDIR /app
COPY --from=builder /root/go/bin/pocketbase /app/pocketbase
EXPOSE 8090
ENTRYPOINT ["./pocketbase", "serve", "--http=0.0.0.0:8090"]
