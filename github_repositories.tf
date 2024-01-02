resource "github_repository" "repos" {
  for_each    = local.repositories
  name        = each.value.name
  description = each.value.description
  visibility  = try(each.value.visibility, "private")
  has_wiki    = try(each.value.has_wiki, false)
  auto_init   = try(each.value.auto_init, true)
  template {
    owner                = "blinqas"
    repository           = "gh-template-station-workload"
    include_all_branches = false
  }
}

locals {
  repositories = {
    example = {
      name        = "station-example-repo"
      description = "Example description"
    }
  }
}