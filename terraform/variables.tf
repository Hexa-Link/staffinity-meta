# variables.tf

variable "github_token" {
  description = "The GitHub Personal Access Token used to authenticate with the GitHub API."
  sensitive   = true
}

variable "target_repositories" {
  description = "A list of repository names to apply the configuration to."
  type        = list(string)
  default = [
    "staffinity-personal-service",
    "staffinity-recruiting-service",
    "staffinity-frontend",
    "staffinity-data"
  ]
}

variable "do_token" {
  description = "DigitalOcean API Token"
  sensitive   = true
}

variable "ssh_public_key" {
  description = "The Public SSH Key to add to the Droplet for access"
  type        = string
}