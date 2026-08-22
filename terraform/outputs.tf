output "rds_endpoint" {
  description = "AWS RDS Instance Endpoint URL"
  value       = aws_db_instance.mysql_rds.endpoint
}

output "rds_db_name" {
  description = "Database Name"
  value       = aws_db_instance.mysql_rds.db_name
}

output "s3_bucket_name" {
  description = "S3 Bucket Name for Media Files"
  value       = aws_s3_bucket.media_bucket.id
}