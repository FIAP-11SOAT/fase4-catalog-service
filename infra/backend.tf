terraform {
  backend "s3" {
    bucket         = "fase4-catalog-service-833984136084-us-east-1-artifacts"
    key            = "terraform/state/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
