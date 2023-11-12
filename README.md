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

In `workload_example-workload.tf`, we have an example module `example_workload` that demonstrates:

- How to specify the Station module source and version.
- Setting up a basic environment and resource group in Azure.
- Configuring a Terraform Cloud workspace with descriptions, VCS repository connections, and branch specifications.
- Creating an Entra ID security group that will available for the new workload.

This example serves as a template to create and manage individual workload environments, each tailored to specific requirements.

### GitHub Repositories Configuration

The `github_repositories.tf` file is responsible for setting up new GitHub repositories for each workload. It defines:

- Repository attributes like name, description, visibility, and initialization settings.
- A template repository from `blinqas/gh-template-station-workload` to standardize the setup of new repositories.


## Getting Started

1. Explore the configuration files to understand their structure and purpose.
2. Modify the example configurations to match your specific deployment requirements.
3. Apply your Terraform configurations to set up the environment in Azure and manage it through Terraform Cloud.

## Need Help?

If you have questions or encounter any issues, please refer to the [Station GitHub page](https://github.com/blinqas/station) for detailed documentation and support resources.

Enjoy creating and managing your environments with Station!
