# main.tf

terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0" # Updated to a more recent version
    }
  }
}

# Configure the provider to use your organization and the personal access token (PAT)
provider "github" {
  owner = "Hexa-Link"
  token = var.github_token # The token will be passed as a variable for security
}