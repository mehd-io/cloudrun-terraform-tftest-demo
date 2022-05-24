output "cloud_run_api_image_name" {
  value = google_cloud_run_service.cloud_run_api_image.name
}

output "cloud_run_api_url" {
  value = google_cloud_run_service.cloud_run_api_image.status[0]["url"]
}
