# infra-snowflake

## Test a Snowflake OIDC connection

The **Snowflake OIDC connection test** workflow can test either the `nonprod` or
`prod` Snowflake account. It uses a GitHub Environment to select the account
configuration without storing environment-specific values in the workflow file.

### Configure GitHub

In **Settings → Environments**, create environments named exactly `nonprod` and
`prod`. In each environment, add the following under **Environment variables**:

| Variable | Value |
| --- | --- |
| `SNOWFLAKE_ACCOUNT` | Account identifier for this environment |
| `SNOWFLAKE_USER` | Snowflake user configured for GitHub OIDC |
| `SNOWFLAKE_ROLE` | Optional role to use for the connection |

The workflow attaches the job to the selected GitHub Environment, making that
environment's variables available to the test script. Environment protection
rules, such as required reviewers, also apply to the selected job.

### Configure Snowflake OIDC trust

The Snowflake security integration must trust GitHub's OIDC tokens for this
repository and both GitHub Environment names. For environment-bound jobs, the
token subject identifies the environment, for example:

- `repo:singhkajal1011/infra-snowflake:environment:nonprod`
- `repo:singhkajal1011/infra-snowflake:environment:prod`

Configure the integration for the `snowflakecomputing.com` audience requested by
the workflow's test script, and ensure the Snowflake user is authorized to connect
with the configured role.

### Run the test

Open **Actions → Snowflake OIDC connection test → Run workflow**, choose
`nonprod` or `prod`, then start the workflow. The run uses only the variables
configured for that environment.