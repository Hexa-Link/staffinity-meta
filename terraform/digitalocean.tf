resource "digitalocean_ssh_key" "default" {
  name       = "hexalink-terraform-key"
  public_key = var.ssh_public_key
}

resource "digitalocean_droplet" "hexalink_mvp" {
  image    = "docker-20-04"
  name     = "hexalink-mvp-droplet"
  region   = "nyc1"
  size     = "s-2vcpu-4gb" # Professional sizing for 2 DBs + 3 Apps
  tags     = ["hexalink", "mvp"]
  ssh_keys = [digitalocean_ssh_key.default.fingerprint]
  
  # user_data to install docker-compose if not present, though docker image usually has docker
  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker-compose
              EOF
}

output "droplet_ip" {
  value = digitalocean_droplet.hexalink_mvp.ipv4_address
}
