# Simple RDS PostgreSQL instance in the default VPC subnets
# For production, prefer private subnets and Multi-AZ, with proper backups.

resource "aws_db_subnet_group" "rds" {
  name        = "${var.project_name}-rds-subnets"
  subnet_ids  = data.aws_subnets.default.ids
  description = "DB subnet group for ${var.project_name}"
}

resource "aws_db_instance" "postgres" {
  identifier        = "${replace(var.project_name, "_", "-")}-pg"
  engine            = "postgres"
  engine_version    = var.rds_engine_version != "" ? var.rds_engine_version : null
  instance_class    = var.rds_instance_class
  allocated_storage = var.rds_allocated_storage
  storage_encrypted = true
  db_name           = var.db_name
  username          = var.db_user
  password          = var.db_pass
  port              = tonumber(var.db_port)

  db_subnet_group_name    = aws_db_subnet_group.rds.name
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]
  multi_az                = var.rds_multi_az
  publicly_accessible     = var.rds_publicly_accessible
  deletion_protection     = var.rds_deletion_protection
  skip_final_snapshot     = var.rds_skip_final_snapshot
  backup_retention_period = var.rds_backup_retention_days

  apply_immediately = true
}
