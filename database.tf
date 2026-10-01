resource "snowflake_database" "source" {
  name    = "SOURCE_${upper(var.environment)}"
  comment = "Source-aligned data database"
}

resource "snowflake_database" "domain" {
  name    = "DOMAIN_${upper(var.environment)}"
  comment = "Domain-aligned data database"
}
