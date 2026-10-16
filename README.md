# infra-snowflake

## Test a Snowflake OIDC connection

The **Snowflake OIDC connection test** workflow has two manual inputs: a tier
(`nonprod` or `prod`) and a stage (`dev`, `sit`, `test`, or `perf`). It combines
them to select a GitHub Environment, such as `nonprod-dev` or `prod-perf`, so
each combination can use its own Snowflake configuration without storing
environment-specific values in the workflow file.

### Configure GitHub

In **Settings → Environments**, create one environment for every tier/stage
combination you intend to run, using the exact lowercase names, for example
`nonprod-dev`, `nonprod-sit`, `nonprod-test`, `nonprod-perf`, and `prod-perf`.
In each environment, add the following under **Environment variables**:

| Variable | Value |
| --- | --- |
| `SNOWFLAKE_ACCOUNT` | Account identifier for this environment |
| `SNOWFLAKE_USER` | Snowflake user configured for GitHub OIDC |
| `SNOWFLAKE_ROLE` | Optional role to use for the connection |

The workflow attaches the job to the combined GitHub Environment name, making
that environment's variables available to the test script. Environment
protection rules, such as required reviewers, also apply to the selected job.

### Configure Snowflake OIDC trust

The Snowflake security integration must trust GitHub's OIDC tokens for this
repository and each GitHub Environment name you use. For environment-bound jobs,
the token subject identifies the combined environment, for example:

- `repo:singhkajal1011/infra-snowflake:environment:nonprod-dev`
- `repo:singhkajal1011/infra-snowflake:environment:prod-perf`

Configure the integration for the `snowflakecomputing.com` audience requested by
the workflow's test script, and ensure the Snowflake user is authorized to connect
with the configured role.

### Run the test

Open **Actions → Snowflake OIDC connection test → Run workflow**, choose a tier
and stage, then start the workflow. The run uses only the variables configured
for the matching combined environment.