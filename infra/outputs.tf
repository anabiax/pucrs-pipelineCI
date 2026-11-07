output "instance_id" {
  description = "ID da instancia EC2"
  value       = aws_instance.app.id
}

output "instance_public_ip" {
  description = "IP publico da instancia"
  value       = aws_instance.app.public_ip
}

output "bucket_artefatos" {
  description = "Bucket S3 de artefatos"
  value       = aws_s3_bucket.artefatos.bucket
}
