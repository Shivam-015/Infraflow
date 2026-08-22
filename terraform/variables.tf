variable "aws_region" {
  description = "AWS Region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment Environment"
  type        = string
  default     = "production"
}

variable "db_name" {
  description = "Name of the RDS database"
  type        = string
  default     = "ecommercedb"
}

variable "db_username" {
  description = "Master username for RDS"
  type        = string
  default     = "dbadmin"
}

variable "db_password" {
  description = "Master password for RDS"
  type        = string
  sensitive   = true
}