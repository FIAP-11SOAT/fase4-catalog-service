data "aws_caller_identity" "current" {}

resource "aws_iam_role" "lambda" {
  name               = "${var.project_name}-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_vpc" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.project_name}"
  retention_in_days = 14
}

# S3 bucket para artefatos (.zip) da Lambda (nome único por conta/região)
resource "aws_s3_bucket" "artifacts" {
  bucket = lower(replace("${var.project_name}-${data.aws_caller_identity.current.account_id}-${var.aws_region}-artifacts", "_", "-"))
}

# Block public access at the account/bucket level
resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Server access logging for S3 bucket
resource "aws_s3_bucket" "artifacts_logs" {
  bucket = lower(replace("${var.project_name}-${data.aws_caller_identity.current.account_id}-${var.aws_region}-artifacts-logs", "_", "-"))
}

resource "aws_s3_bucket_public_access_block" "artifacts_logs" {
  bucket = aws_s3_bucket.artifacts_logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_logging" "artifacts" {
  bucket        = aws_s3_bucket.artifacts.id
  target_bucket = aws_s3_bucket.artifacts_logs.id
  target_prefix = "access-logs/"
}

# Enforce HTTPS-only access to artifacts bucket
resource "aws_s3_bucket_policy" "artifacts_https_only" {
  bucket = aws_s3_bucket.artifacts.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid      = "DenyInsecureTransport",
        Effect   = "Deny",
        Principal = "*",
        Action   = "s3:*",
        Resource = [
          aws_s3_bucket.artifacts.arn,
          "${aws_s3_bucket.artifacts.arn}/*"
        ],
        Condition = {
          Bool = {"aws:SecureTransport" = false}
        }
      }
    ]
  })
}

locals {
  vpc_subnet_ids_csv_clean         = replace(var.vpc_subnet_ids_csv, " ", "")
  vpc_security_group_ids_csv_clean = replace(var.vpc_security_group_ids_csv, " ", "")

  # Se não vier via var/list/CSV, usa as subnets do VPC default
  vpc_subnet_ids_effective = length(var.vpc_subnet_ids) > 0 ? var.vpc_subnet_ids : (
    var.vpc_subnet_ids_csv != "" ? split(",", local.vpc_subnet_ids_csv_clean) : try(data.aws_subnets.default.ids, [])
  )

  # Se não vier via var/list/CSV, usa o SG da Lambda criado neste módulo
  vpc_security_group_ids_effective = length(var.vpc_security_group_ids) > 0 ? var.vpc_security_group_ids : (
    var.vpc_security_group_ids_csv != "" ? split(",", local.vpc_security_group_ids_csv_clean) : (
      try([aws_security_group.lambda_sg.id], [])
    )
  )
}

resource "aws_lambda_function" "app" {
  function_name = var.project_name
  role          = aws_iam_role.lambda.arn
  runtime       = "python3.11"
  handler       = "app.main.handler"
  architectures = ["x86_64"]
  memory_size   = var.memory_size
  timeout       = var.timeout

  # Código a partir de artefato no S3 (gerado pelo pipeline)
  s3_bucket         = aws_s3_bucket.artifacts.bucket
  s3_key            = var.artifact_key
  s3_object_version = var.artifact_object_version != "" ? var.artifact_object_version : null

  environment {
    variables = {
      DB_HOST = var.db_host != "" ? var.db_host : aws_db_instance.postgres.address
      DB_PORT = var.db_port
      DB_NAME = var.db_name
      DB_USER = var.db_user
      DB_PASS = var.db_pass
    }
  }

  dynamic "vpc_config" {
    for_each = length(local.vpc_subnet_ids_effective) > 0 && length(local.vpc_security_group_ids_effective) > 0 ? [1] : []
    content {
      subnet_ids         = local.vpc_subnet_ids_effective
      security_group_ids = local.vpc_security_group_ids_effective
    }
  }

  depends_on = [aws_iam_role_policy_attachment.lambda_logs, aws_iam_role_policy_attachment.lambda_vpc]
}

resource "aws_apigatewayv2_api" "http" {
  name          = "${var.project_name}-http"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.app.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "root" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "ANY /"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_route" "proxy" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.lambda.arn
    format          = jsonencode({
      requestId = "$context.requestId",
      ip        = "$context.identity.sourceIp",
      request   = "$context.httpMethod $context.path",
      status    = "$context.status"
    })
  }
}

resource "aws_lambda_permission" "apigw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.app.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}
