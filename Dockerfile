# Etapa build: compilar PocketBase a partir de tu código local
FROM golang:1.20-alpine AS builder

# Instala dependencias necesarias
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copia únicamente los ficheros de módulos para aprovechar la cache de Docker
COPY go.mod go.sum ./
RUN go mod download

# Copia todo tu código local de PocketBase
COPY . .

# Compila el binario de PocketBase
# Ajusta la ruta si tu comando principal está en otro paquete
RUN go build -o pocketbase ./cmd/pocketbase

# Etapa runtime: contenedor ligero con el binario ya compilado
FROM alpine:latest

RUN apk add --no-cache ca-certificates

WORKDIR /app

# Copia el binario desde la etapa builder
COPY --from=builder /app/pocketbase /app/pocketbase

# (Opcional) copia tu carpeta de datos si la quieres versionar o inicializar
# COPY pb_data /app/pb_data

EXPOSE 8090

ENTRYPOINT ["/app/pocketbase", "serve", "--http=0.0.0.0:8090"]
