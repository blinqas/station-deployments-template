variable "vcs_repo_oauth_token_id" {
  type        = string
  sensitive   = true
  description = "OAuth Token ID for GitHub - used to authenticate workspaces to repositories."
  nullable    = true
}

variable "vcs_repo_github_app_installation_id" {
  type        = string
  sensitive   = true
  description = "OAuth Token ID for GitHub - used to authenticate workspaces to repositories. This is an alternative for vcs_repo_oauth_token_id"
  nullable    = true
}
# You can not use both the vcs_repo_github_app_installation_id and the vcs_repo_oauth_token_id. Choose the one you used during the bootstrap process and the delete the one you dont need.