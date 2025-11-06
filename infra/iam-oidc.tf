# GitHub OIDC provider and IAM Role for GitHub Actions to assume
# Reference: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services

# OIDC provider for GitHub
resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com"
  ]

  # Well-known thumbprint for GitHub OIDC root CA (as of Nov/2025)
  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1"
  ]
}

# IAM Role to be assumed by GitHub Actions
locals {
  # Se 'gh_branches' vier preenchido, autoriza todas; senão, só 'gh_branch'
  gh_allowed_subs = length(var.gh_branches) > 0 ? [for b in var.gh_branches : "repo:${var.gh_owner}/${var.gh_repo}:ref:refs/heads/${b}"] : [
    "repo:${var.gh_owner}/${var.gh_repo}:ref:refs/heads/${var.gh_branch}"
  ]
}

resource "aws_iam_role" "github_actions" {
  name = var.oidc_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRoleWithWebIdentity"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        }
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            # Restringe a este repo e às branches permitidas
            "token.actions.githubusercontent.com:sub" = local.gh_allowed_subs
          }
        }
      }
    ]
  })
}

# Minimal policy for this repo's Terraform (can be tightened further)
# In PoC, you can set var.attach_admin_policy=true to attach AdministratorAccess instead.
resource "aws_iam_policy" "github_actions_deploy" {
  name        = "${var.project_name}-deploy-policy"
  description = "Permissions for Terraform to deploy Lambda/API/S3/RDS/EC2/Logs"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:CreateBucket", "s3:PutBucketVersioning", "s3:GetBucketVersioning",
          "s3:ListAllMyBuckets", "s3:ListBucket", "s3:GetBucketLocation",
          "s3:PutObject", "s3:GetObject", "s3:HeadObject"
        ],
        Resource = ["*"]
      },
      {
        Effect = "Allow",
        Action = [
          "iam:CreateRole", "iam:GetRole", "iam:AttachRolePolicy", "iam:PutRolePolicy"
        ],
        Resource = ["*"]
      },
      {
        Effect = "Allow",
        Action = ["iam:PassRole"],
        Resource = [
          "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.project_name}-lambda-role"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "lambda:CreateFunction", "lambda:UpdateFunctionCode", "lambda:UpdateFunctionConfiguration",
          "lambda:GetFunction", "lambda:ListFunctions", "lambda:DeleteFunction",
          "lambda:AddPermission", "lambda:RemovePermission"
        ],
        Resource = ["*"]
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup", "logs:PutRetentionPolicy", "logs:DescribeLogGroups"
        ],
        Resource = ["*"]
      },
      {
        Effect = "Allow",
        Action = [
          "apigateway:*", "execute-api:Invoke"
        ],
        Resource = ["*"]
      },
      {
        Effect = "Allow",
        Action = [
          "ec2:CreateSecurityGroup", "ec2:DeleteSecurityGroup",
          "ec2:AuthorizeSecurityGroupIngress", "ec2:AuthorizeSecurityGroupEgress",
          "ec2:RevokeSecurityGroupIngress", "ec2:RevokeSecurityGroupEgress",
          "ec2:CreateTags",
          "ec2:DescribeVpcs", "ec2:DescribeSubnets", "ec2:DescribeSecurityGroups", "ec2:DescribeRouteTables",
          "ec2:DescribeVpcAttribute", "ec2:DescribeAccountAttributes"
        ],
        Resource = ["*"]
      },
      {
        Effect = "Allow",
        Action = [
          "rds:CreateDBInstance", "rds:DeleteDBInstance", "rds:ModifyDBInstance", "rds:DescribeDBInstances",
          "rds:ListTagsForResource", "rds:AddTagsToResource",
          "rds:CreateDBSubnetGroup", "rds:DeleteDBSubnetGroup", "rds:ModifyDBSubnetGroup", "rds:DescribeDBSubnetGroups"
        ],
        Resource = ["*"]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "github_actions_deploy_attach" {
  count      = var.attach_admin_policy ? 0 : 1
  role       = aws_iam_role.github_actions.name
  policy_arn = aws_iam_policy.github_actions_deploy.arn
}

# Optional: attach AdministratorAccess for PoC
resource "aws_iam_role_policy_attachment" "github_actions_admin" {
  count      = var.attach_admin_policy ? 1 : 0
  role       = aws_iam_role.github_actions.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

output "github_actions_role_arn" {
  description = "IAM Role ARN for GitHub Actions OIDC"
  value       = aws_iam_role.github_actions.arn
}
