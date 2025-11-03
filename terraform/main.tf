terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "flask_app" {
  name = "flask_app_image:latest"

  build {
    context    = "${path.module}/../app"
    dockerfile = "Dockerfile"
  }
}

resource "docker_container" "flask_app_container" {
  name  = "flask_app_container"
  image = "flask_app_image:latest"

  ports {
    internal = 5000
    external = 5000
  }

  mounts {
    type   = "bind"
    source = abspath("${path.module}/../logs")
    target = "/logs"
  }
}
