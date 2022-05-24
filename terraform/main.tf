provider "google" {
  project = var.gcp_project_id
}

data "google_project" "project" {
  project_id = var.gcp_project_id
}

resource "google_project_service" "cloudrun_api_google_services" {
  for_each = toset([
    "secretmanager.googleapis.com",
    "containerregistry.googleapis.com",
    "run.googleapis.com"
  ])
  service            = each.key
  project            = var.gcp_project_id
  disable_on_destroy = false
}

resource "google_service_account" "cloudrun_api_service_account" {
  account_id   = var.gcp_service_account_name
  display_name = "Demo service account used name by Cloud Run"
  project      = var.gcp_project_id
}

resource "google_project_iam_member" "cloudrun_api_service_account_roles" {
  for_each = toset([
      "roles/editor",
    "roles/secretmanager.secretAccessor"
  ])
  role       = each.key
  project    = var.gcp_project_id
  member     = "serviceAccount:${google_service_account.cloudrun_api_service_account.email}"
  depends_on = [google_service_account.cloudrun_api_service_account]
}

resource "null_resource" "build_and_push_docker_image" {
  triggers = {
    always_run = timestamp()
  }
  depends_on = [google_project_service.cloudrun_api_google_services, null_resource.build_and_push_docker_image]

  provisioner "local-exec" {
    command = "bash ${path.module}/scripts/build_push_docker_img.sh gcr.io/${var.gcp_project_id}/${var.prefix} latest ${var.gcp_region}"
  }
}

resource "google_cloud_run_service" "cloud_run_api_image" {
  name       = "${var.prefix}-cloudrun-api"
  location   = var.gcp_region
  depends_on = [null_resource.build_and_push_docker_image, google_project_service.cloudrun_api_google_services, google_service_account.cloudrun_api_service_account]

  template {
    spec {
      containers {
        image = "gcr.io/${var.gcp_project_id}/${var.prefix}:latest"

      }
      service_account_name = google_service_account.cloudrun_api_service_account.email
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}
