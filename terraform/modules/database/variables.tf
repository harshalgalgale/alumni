variable project {
  type        = string
  description = "The Google Cloud Platform project name"
  default     = "learn-terraform-311311"
}

variable service {
  description = "Name of the service"
  type        = string
}

variable region {
  default = "europe-west2"
  type    = string
}

variable instance_name {
  description = "Name of the postgres instance (PROJECT_ID:REGION:INSTANCE_NAME))"
  type        = string
  default     = "learn-terraform-311311:europe-west2:unicodex-sql"
}

