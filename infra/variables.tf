variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name prefix for resources (also ECR repo name)"
  type        = string
  default     = "fase4-catalog-service"
}

variable "artifact_key" {
  description = "S3 object key (path) do pacote .zip a ser implantado na Lambda (ex.: releases/commit-sha.zip)"
  type        = string
  default     = ""
}

variable "artifact_object_version" {
  description = "Versão do objeto S3 (se bucket com versioning habilitado)"
  type        = string
  default     = ""
}

variable "memory_size" {
  description = "Lambda memory size (MB)"
  type        = number
  default     = 512
}

variable "timeout" {
  description = "Lambda timeout (seconds)"
  type        = number
  default     = 30
}

variable "db_host" {
  type        = string
  description = "Database host. Deixe vazio para usar o endpoint do RDS criado pelo Terraform."
  default     = ""
}

variable "db_port" {
  type        = string
  description = "Database port"
  default     = "5432"
}

variable "db_name" {
  type        = string
  description = "Database name"
  default     = "postgres"
}

variable "db_user" {
  type        = string
  description = "Database user"
  default     = "postgres"
}

variable "db_pass" {
  type        = string
  description = "Database password"
  default     = "postgres"
  sensitive   = true
}

variable "vpc_subnet_ids" {
  type        = list(string)
  description = "Optional list of subnet IDs for Lambda VPC configuration"
  default     = []
}

variable "vpc_security_group_ids" {
  type        = list(string)
  description = "Optional list of security group IDs for Lambda VPC configuration"
  default     = []
}

variable "vpc_subnet_ids_csv" {
  type        = string
  description = "Optional CSV of subnet IDs (alternative to list var)"
  default     = ""
}

variable "vpc_security_group_ids_csv" {
  type        = string
  description = "Optional CSV of security group IDs (alternative to list var)"
  default     = ""
}

# --- RDS (Postgres) ---
variable "rds_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "rds_allocated_storage" {
  description = "RDS allocated storage (GB)"
  type        = number
  default     = 20
}

variable "rds_engine_version" {
  description = "PostgreSQL engine version. Deixe vazio para usar a versão padrão recomendada pela AWS (evita erros quando uma versão específica sai de linha). Exemplos suportados comuns: '16.4', '15.7'"
  type        = string
  default     = ""
}

variable "rds_multi_az" {
  description = "Enable Multi-AZ (prod)"
  type        = bool
  default     = false
}

variable "rds_backup_retention_days" {
  description = "Backup retention days (0 = disabled)"
  type        = number
  default     = 0
}

variable "rds_publicly_accessible" {
  description = "Whether RDS should be publicly accessible"
  type        = bool
  default     = true
}

variable "rds_deletion_protection" {
  description = "Enable deletion protection (disable for dev)"
  type        = bool
  default     = false
}

variable "rds_skip_final_snapshot" {
  description = "Skip final snapshot on destroy (true for dev)"
  type        = bool
  default     = true
}

# --- GitHub OIDC (para CI/CD) ---
variable "gh_owner" {
  description = "GitHub org/owner"
  type        = string
  default     = "FIAP-11SOAT"
}

variable "gh_repo" {
  description = "GitHub repository name"
  type        = string
  default     = "fase4-catalog-service"
}

variable "gh_branch" {
  description = "Branch do GitHub Actions autorizado a assumir a role"
  type        = string
  default     = "feat/catalog-service"
}

# Permite autorizar múltiplas branches para OIDC. Se vazio, usa apenas gh_branch.
variable "gh_branches" {
  description = "Lista de branches do GitHub Actions autorizadas a assumir a role via OIDC"
  type        = list(string)
  default     = []
}

variable "oidc_role_name" {
  description = "Nome da IAM Role a ser assumida pelo GitHub Actions via OIDC"
  type        = string
  default     = "github-actions-deploy-role"
}

variable "attach_admin_policy" {
  description = "Anexa AdministratorAccess à role OIDC (útil para PoC). Se false, anexa política mínima gerada."
  type        = bool
  default     = false
}
