# pucrs-pipelineCI

Projeto da disciplina de DevOps (PUCRS Online): pipeline de Integração Contínua com GitHub Actions e Infraestrutura como Código com Terraform.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `app/` | Aplicação Python (gerenciador de tarefas) |
| `tests/` | Testes automatizados (pytest) |
| `.github/workflows/ci.yml` | Pipeline de CI (GitHub Actions) |
| `infra/` | Scripts Terraform (EC2, Security Group, S3) |

## Executar localmente

```bash
pip install -r requirements.txt
flake8 app tests
pytest --cov=app
```

## Pipeline de CI

Executado a cada `push` e `pull request` na branch `main`:

1. Checkout do código
2. Instalação de dependências (Python 3.11 e 3.12)
3. Lint com flake8
4. Testes com pytest e cobertura mínima de 80%
5. Validação do Terraform (`fmt`, `init`, `validate`)

## Infraestrutura (Terraform)

```bash
cd infra
terraform init
terraform plan -var="ssh_allowed_cidr=SEU_IP/32"
terraform apply -var="ssh_allowed_cidr=SEU_IP/32"
```

Requer credenciais AWS configuradas (`aws configure`).

## Entrega Contínua e Containers (Fase 2)

```bash
docker build -t pucrs-pipelineci .
docker run -p 8000:8000 pucrs-pipelineci      # http://localhost:8000/health
IMAGE=ghcr.io/anabiax/pucrs-pipelineci:latest ./scripts/deploy.sh
```

O pipeline (`ci.yml`) passa a ter os jobs `docker-build` (publica a imagem no GHCR) e `deploy` (SSH na EC2 executando `scripts/deploy.sh`, apenas na `main`). Segredos/variáveis: `DEPLOY_SSH_KEY` (secret) e `DEPLOY_HOST` (variable).