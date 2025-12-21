locals {
  db_host     = local.aws_infra_secrets["RDS_HOST"]
  db_name     = postgresql_database.app_db.name
  db_user     = postgresql_role.app_db_user.name
  db_password = random_password.app_db_password.result
}

resource "github_actions_secret" "database_url" {
  repository      = local.project_name
  secret_name     = "DATABASE_URL"
  plaintext_value = "jdbc:postgresql://${local.db_host}:5432/${local.db_name}?sslmode=require"
}

resource "github_actions_secret" "database_user" {
  repository      = local.project_name
  secret_name     = "DATABASE_USER"
  plaintext_value = local.db_user
}

resource "github_actions_secret" "database_password" {
  repository      = local.project_name
  secret_name     = "DATABASE_PASSWORD"
  plaintext_value = local.db_password
}