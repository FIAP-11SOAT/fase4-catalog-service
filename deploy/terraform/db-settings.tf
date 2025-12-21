resource "random_password" "app_db_password" {
  length  = 16
  special = false
}

resource "postgresql_role" "app_db_user" {
  name     = "${local.project_name}-user"
  login    = true
  password = random_password.app_db_password.result
}

resource "postgresql_database" "app_db" {
  name              = "${local.project_name}-db"
  owner             = postgresql_role.app_db_user.name
  lc_collate        = "en_US.UTF-8"
  lc_ctype          = "en_US.UTF-8"
  allow_connections = true
}

resource "postgresql_default_privileges" "app_db_privileges" {
  role     = postgresql_role.app_db_user.name
  database = postgresql_database.app_db.name
  schema   = "public"

  owner       = postgresql_role.app_db_user.name
  object_type = "table"
  privileges  = ["ALL"]
}