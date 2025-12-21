provider "aws" {
  region = local.aws_region

  default_tags {
    tags = {
      Team      = "mfava"
      Project   = local.project_name
      Terraform = "true"
    }
  }
}

provider "postgresql" {
  host            = local.aws_infra_secrets["RDS_HOST"]
  port            = 5432
  database        = local.aws_infra_secrets["RDS_DATABASE"]
  username        = local.aws_infra_secrets["RDS_USERNAME"]
  password        = local.aws_infra_secrets["RDS_PASSWORD"]
  sslmode         = "require"
  connect_timeout = 15
  superuser       = false
}

provider "github" {
  token = local.aws_master_secrets["GITHUB_ACCESS_TOKEN"]
  owner = local.aws_master_secrets["GITHUB_ORG"]
}