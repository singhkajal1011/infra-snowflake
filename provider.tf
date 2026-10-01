terraform {
  required_version = ">= 1.8.0"

  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 2.0"
    }
  }
}

provider "snowflake" {
  organization_name = var.organization_name
  account_name      = var.account_name
}
