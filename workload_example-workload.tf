module "example_workload" {
  source              = "git::https://github.com/blinqas/station.git?ref=${module_version}"
  environment_name    = "prod"
  resource_group_name = "example-workload"
  tags                = local.tags.common
  
  tfe = {
    organization_name     = "Your-TFC-Org"
    project_name          = "Station"
    workspace_name        = "Example_workload_prod"
    workspace_description = "Your description of the workload for TFC"
    vcs_repo = {
      identifier     = github_repository.repos["example"].full_name
      branch         = "trunk"
      oauth_token_id = var.vcs_repo_oauth_token_id #This can also be replaced with var.vcs_repo_github_app_installation_id if thats how you have configured the authenication
    }
    module_outputs_to_workspace_var = {
      groups = true #This will output the groups you create to the workloads TFC as a variable you can reference in the workloads terraform code.
    }
  }
  # We create a basic Entra ID securtiy group that can be used by the workload
  groups = {
    example_group = {
      display_name     = "A group created by station deployments"
      security_enabled = true
    }
  }
}