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
    "spring.datasource.url"               = "jdbc:postgresql://${local.aws_infra_secrets["RDS_HOST"]}:5432/${postgresql_database.app_db.name}"
    "spring.datasource.username"          = postgresql_role.app_db_user.name
    "spring.datasource.password"          = random_password.app_db_password.result
    "spring.datasource.driver-class-name" = "org.postgresql.Driver"
    "fase4.catalog.service.apigateway.url"  = "https://api.fase4.com"
    "fase4.catalog.service.auth.jwk"        = local.aws_infra_secrets["JWT_JWK"]
  }
}

resource "aws_secretsmanager_secret_version" "secrets" {
  secret_id     = aws_secretsmanager_secret.secrets.id
  secret_string = jsonencode(local.prod_secrets)
}
