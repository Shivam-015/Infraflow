# Default VPC Lookup
resource "aws_default_vpc" "default" {
  tags = {
    Name = "infraflow-default-vpc"
  }
}

# Security Group for Database
resource "aws_security_group" "rds_sg" {
  name        = "infraflow-rds-sg"
  description = "Allow MySQL traffic from EKS/K8s cluster"
  vpc_id      = aws_default_vpc.default.id

  ingress {
    description = "MySQL access"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Tighten to K8s Node CIDR in production
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "infraflow-rds-sg"
    Environment = var.environment
  }
}

# AWS RDS MySQL Instance
resource "aws_db_instance" "mysql_rds" {
  allocated_storage      = 20
  max_allocated_storage  = 50
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  parameter_group_name   = "default.mysql8.0"
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot    = true
  publicly_accessible    = true

  tags = {
    Name        = "infraflow-rds-instance"
    Environment = var.environment
  }
}

# S3 Bucket for Django Dynamic Media Uploads
resource "aws_s3_bucket" "media_bucket" {
  bucket        = "infraflow-media-assets-${var.environment}"
  force_destroy = true

  tags = {
    Name        = "infraflow-media-assets"
    Environment = var.environment
  }
}

# S3 Public Access Block Config
resource "aws_s3_bucket_public_access_block" "media_bucket_public_access" {
  bucket = aws_s3_bucket.media_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}