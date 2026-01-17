# Dockerfile Securise - Architecture Multi-stage avec Distroless
# Template de reference pour applications Go/Java/Node.js

# =============================================================================
# ETAPE 1 : BUILD
# =============================================================================
FROM golang:1.22-alpine AS builder

# Installer les certificats CA pour HTTPS
RUN apk add --no-cache ca-certificates tzdata

# Creer un utilisateur non-root pour le build
RUN addgroup -S buildgroup && adduser -S builduser -G buildgroup

WORKDIR /build

# Copier les fichiers de dependances en premier (cache Docker)
COPY go.mod go.sum ./
RUN go mod download

# Copier le code source
COPY . .

# Compiler en mode statique (pas de dependances glibc)
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags='-w -s -extldflags "-static"' \
    -o /app/server .

# =============================================================================
# ETAPE 2 : RUNTIME (Image Finale)
# =============================================================================
FROM gcr.io/distroless/static-debian12:nonroot

# Labels de securite
LABEL org.opencontainers.image.source="https://github.com/example/app"
LABEL org.opencontainers.image.description="Application securisee avec distroless"
LABEL security.hardened="true"

# Copier les certificats CA
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copier le timezone data
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo

# Copier le binaire compile
COPY --from=builder /app/server /app/server

# L'image distroless:nonroot utilise deja UID 65532
# Pas besoin de USER instruction

# Port d'ecoute (documentaire)
EXPOSE 8080

# Point d'entree
ENTRYPOINT ["/app/server"]

# =============================================================================
# NOTES DE SECURITE
# =============================================================================
# - Image distroless : pas de shell, pas de gestionnaire de paquets
# - Variante 'nonroot' : s'execute en tant qu'utilisateur non-root par defaut
# - Build statique : aucune dependance runtime
# - Multi-stage : le code source et les outils de build ne sont pas dans l'image finale
# - Taille finale : ~20-30 MB selon l'application
