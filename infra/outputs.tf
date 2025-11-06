output "api_url" {
  description = "HTTP API invoke URL"
  value       = aws_apigatewayv2_api.http.api_endpoint
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.app.function_name
}

output "artifacts_bucket" {
  description = "S3 bucket onde os artefatos (.zip) são armazenados"
  value       = aws_s3_bucket.artifacts.bucket
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = aws_db_instance.postgres.address
}

output "rds_port" {
  description = "RDS port"
  value       = aws_db_instance.postgres.port
}
