# Welcome to Station Deployments

## Introduction

Welcome to your Station Deployments repository! This repository, automatically created as part of your Station bootstrap process, includes a basic example to guide you through using Station, a Terraform module for deploying automated environments in Azure.

## Current Repository Structure

- `github_repositories.tf`: Manages the creation of GitHub repositories for your workloads.
- `providers.tf`: Configures the Terraform providers required for your deployments.
- `README.md`: This document.
- `variables.tf`: Defines essential variables for your Terraform configurations.
- `workload_example-workload.tf`: A basic example of a Station workload configuration.

## Understanding the Example Workload Configuration

In the `workload_example-workload.tf` file, the `example_workload` module is provided as an illustrative example that demonstrates how to create a new workload. This is what the file would create/do:

- **Resource Group**: Establishes a resource group in Azure for the workload.
- **Managed Identity**: Creates a managed identity with the Service Principal assigned as Owner on the resource group.
- **Federated Credential**: Sets up a Federated Credential for OIDC to authenticate Terraform Cloud runners.
- **Terraform Cloud (TFC) Workspace**:
  - Configured to run on commits to the trunk branch.
  - Configured to authenticate to VCS with a token already present in Terraform Cloud.
- **TFC Environment Variables**: Sets up environment variables for OIDC authentication with the Managed Identity.
- **Entra ID Security Group**: Creates a new security group that can be used/referenced by the workload.

This example serves as a comprehensive template to create and manage individual workload environments, each tailored to specific requirements.


### GitHub Repositories Configuration

The `github_repositories.tf` file is responsible for setting up new GitHub repositories for each workload. It defines:

- Repository attributes like name, description, visibility, and initialization settings.
- A template repository from `blinqas/gh-template-station-workload` to standardize the setup of new repositories.


## Getting Started

1. Explore the configuration files to understand their structure and purpose.
2. Modify the example configurations to match your specific deployment requirements.
3. Apply your Terraform configurations to set up the environment in Azure and manage it through Terraform Cloud.


## Security Recommendations

When using Station, given that the identity running the Terraform plan and apply commands has Global Administrator access, we strongly recommend the following security practices for enhanced protection:

### Limit Access to the Repository

- **Restricted Access**: Limit the number of users who have access to this repository. Only team members who need to deploy new workload environments should have access.
- **Two-Factor Authentication (2FA)**: Ensure all users with access to this repository have enabled 2FA. This adds an extra layer of security against unauthorized access.

### Disable Auto Apply in Terraform Cloud

- **Manual Review of Changes**: We advise not enabling auto apply in TFC. This practice ensures that all changes undergo manual review and approval before they are applied, reducing the risk of unintended or malicious alterations.

### Protect the Trunk Branch

- **Branch Protection Rules**: Implement branch protection on the trunk branch to prevent direct pushes. Changes should only be made via pull requests.
- **Mandatory Code Reviews**: Require pull request reviews for all changes. This adds an additional layer of security, ensuring every modification is thoroughly vetted by at least one other team member before merging.

### Acknowledge the Risks

- **Risk Awareness**: Ensure that all users with access to this repository understand the risks associated.

Following these security recommendations will greatly enhance the safety and integrity of your Station deployments, ensuring they are managed securely and responsibly.


## Need Help?

If you have questions or encounter any issues, please refer to the [Station GitHub page](https://github.com/blinqas/station) for detailed documentation and support resources.

Enjoy creating and managing your environments with Station!
