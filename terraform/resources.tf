# resources.tf

# --- RESOURCE 1: Create CODEOWNERS file in each repository ---

resource "github_repository_file" "codeowners_file" {
  # Loop over the list of repositories defined in variables.tf
  for_each = toset(var.target_repositories)

  repository          = each.key
  branch              = "main" # Assumes 'main' is the default branch
  file                = ".github/CODEOWNERS"
  content             = "* @Hexa-Link/owners"
  commit_message      = "feat: Add CODEOWNERS file"
  overwrite_on_create = true
}


# --- RESOURCE 2: Define Branch Protection Rules for 'develop' ---

resource "github_branch_protection" "develop_branch_rules" {
  for_each = toset(var.target_repositories)


  repository_id = each.key
  pattern    = "develop"

  enforce_admins = true

  required_pull_request_reviews {
    required_approving_review_count = 2
    require_code_owner_reviews      = true
  }


  required_status_checks {
    strict = true
  }
}


# --- RESOURCE 3: Define Branch Protection Rules for 'main' ---

resource "github_branch_protection" "main_branch_rules" {
  for_each = toset(var.target_repositories)


  repository_id = each.key
  pattern    = "main"

  enforce_admins = true

  allows_force_pushes = false
  allows_deletions    = false


  required_pull_request_reviews {
    required_approving_review_count = 3
    require_code_owner_reviews      = true
  }
}