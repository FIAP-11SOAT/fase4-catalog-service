terraform {
  required_version = ">= 1.11.0"

  backend "s3" {
    bucket = "fase4-terraform-state"
    key    = "fase4-catalog-service/terraform.tfstate"
    region = "us-east-1"
  }

  required_providers {

    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.14.1"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.7.2"
    }

    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "~> 1.21.0"
    }

    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }

  }
}