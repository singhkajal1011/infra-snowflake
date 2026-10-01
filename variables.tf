variable "environment" {
  description = "Deployment environment"
  type        = string

  validation {
    condition     = contains(["dev", "test", "uat"], var.environment)
    error_message = "Environment must be dev, test or uat."
  }
}

variable "organization_name" {
  type = string
}

variable "account_name" {
  type = string
}

variable "default_warehouse_size" {
  type    = string
  default = "XSMALL"
}
