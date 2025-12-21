resource "aws_secretsmanager_secret" "secrets" {
  name                    = "${local.project_name}-secrets"
  description             = "Secrets for ${local.project_name} project"
  recovery_window_in_days = 0

  tags = {
    Name = "${local.project_name}-secrets"
  }
}

locals {
  prod_secrets = {
    "spring.datasource.url"               = "jdbc:postgresql://prod-db-host:5432/prod_db"
    "spring.datasource.username"          = "prod_user"
    "spring.datasource.password"          = "prod_password"
    "spring.datasource.driver-class-name" = "org.postgresql.Driver"
    "fase4.catalog.service.apigateway.url"  = "https://api.fase4.com"
    "fase4.catalog.service.auth.jwk"        = ""
  }
}

resource "aws_secretsmanager_secret_version" "secrets" {
  secret_id     = aws_secretsmanager_secret.secrets.id
  secret_string = jsonencode(local.prod_secrets)
}
