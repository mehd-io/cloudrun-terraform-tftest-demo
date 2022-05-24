variable "gcp_service_account_name" {
  description = "Demo API service account name used by Cloud Run"
  type        = string
  default     = "demo-tftest"
}

variable "gcp_project_id" {
  description = "Demo API service account name used by Cloud Run"
  type        = string
  default     = "seraphic-cocoa-351210"
}

variable "prefix" {
  description = "Demo API service account name used by Cloud Run"
  type        = string
  default     = "demo-api"
}

variable "gcp_region" {
  description = "Demo API service account name used by Cloud Run"
  type        = string
  default     = "europe-west1"
}
