terraform {
  required_version = "~> 1.6"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }

    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.45"
    }

    tfe = {
      source  = "hashicorp/tfe"
      version = "~> 0.50"
    }

    github = {
      source  = "integrations/github"
      version = "~> 5.42"
    }
  }
  # Enables init, validate and plan from the CLI
  # Documentation: https://developer.hashicorp.com/terraform/cli/cloud/settings
  # 
  # Set the following environment variables before you run terraform init.
  # - TF_CLOUD_ORGANIZATION: "Your TFC org name"
  # - TF_WORKSPACE: Current-Workspace
  cloud {}
}

provider "azurerm" {
  features {}
}

provider "azuread" {}

provider "tfe" {
  # Configuration options
}

# GitHub is authenticated with the GITHUB_TOKEN environment variable.
# https://registry.terraform.io/providers/integrations/github/latest/docs#oauth--personal-access-token
provider "github" {
  # Configuration options
}