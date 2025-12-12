# main.tf

terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

# Configure the provider to use your organization and the personal access token (PAT)
provider "github" {
  owner = "Hexa-Link"
  token = var.github_token # The token will be passed as a variable for security
}