#!/usr/bin/env bash
# Deploy da aplicação em container.
# Uso: IMAGE=ghcr.io/anabiax/pucrs-pipelineci:<tag> ./scripts/deploy.sh
set -euo pipefail

IMAGE="${IMAGE:-ghcr.io/anabiax/pucrs-pipelineci:latest}"
export IMAGE
cd "$(dirname "$0")/.."

if ! command -v docker >/dev/null 2>&1; then
  echo ">> Docker não encontrado; instalando..."
  sudo dnf install -y docker
  sudo systemctl enable --now docker
fi

if ! docker compose version >/dev/null 2>&1; then
  echo ">> Docker Compose não encontrado; instalando..."
  sudo mkdir -p /usr/local/lib/docker/cli-plugins
  sudo curl -fsSL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
    -o /usr/local/lib/docker/cli-plugins/docker-compose
  sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
fi

echo ">> Baixando imagem ${IMAGE}"
docker pull "${IMAGE}"

echo ">> Subindo container"
docker compose up -d --no-build --remove-orphans

echo ">> Verificando saúde da aplicação"
for i in $(seq 1 15); do
  if curl -fsS http://localhost/health >/dev/null; then
    echo ">> Deploy concluído com sucesso."
    exit 0
  fi
  sleep 2
done

echo "!! A aplicação não respondeu ao health check." >&2
docker compose logs --tail=50 >&2
exit 1
