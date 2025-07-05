resource "google_service_account" "secret_sync" {
  account_id   = "secret-sync"
  display_name = "Secret Sync Service Account"
}

resource "google_project_iam_member" "secret_manager_editor" {
  project = var.project_id
  role    = "roles/secretmanager.admin"
  member  = "serviceAccount:${google_service_account.secret_sync.email}"
}
