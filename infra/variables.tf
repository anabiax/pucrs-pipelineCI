variable "aws_region" {
  description = "Regiao AWS"
  type        = string
  default     = "sa-east-1"
}

variable "project_name" {
  description = "Nome do projeto, usado como prefixo dos recursos"
  type        = string
  default     = "pucrs-pipelineci"
}

variable "environment" {
  description = "Ambiente (dev, hml, prd)"
  type        = string
  default     = "dev"
}

variable "instance_type" {
  description = "Tipo da instancia EC2"
  type        = string
  default     = "t3.micro"
}

variable "ssh_allowed_cidr" {
  description = "CIDR autorizado a acessar via SSH (restrinja ao seu IP)"
  type        = string
  default     = "0.0.0.0/32"
}
