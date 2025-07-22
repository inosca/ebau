# camac-ng tools

## Upload RSTA Templates

Command to distribute RSTA template files

```bash
TOKEN="Bearer xy" pnpm upload-rsta-templates
```

| Argument      | Description                                                                                    | Default                                                        |
| ------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `pattern`     | Glob pattern of file(s) to upload                                                              | `../document-merge-service/kt_bern/rsta_templates/**/*.docx`   |
| `groups`      | Comma-separated list of groups to upload to (your token has to be valid for all of them!)      | Preconfigured list of RSTA admin groups for dev and production |
| `environment` | Environment to upload to, can be `local`, `test` or `prod`                                     | `local`                                                        |
| `token`       | The OIDC token to authorize                                                                    | `process.env.TOKEN`                                            |
| `skip-patch`  | Skip all updates, only upload new templates                                                    | `false`                                                        |
| `delete`      | Delete all existing templates that have match the RSTA prefixes: `/^(bpv\|nhhe\|nhsb\|rsta)_/` | `false`                                                        |
| `dry-run`     | Show what would be done without actually doing requests                                        | `false`                                                        |

## Alexandria permissions tables

You can use the `dump-alexandria-permissions.js` script to create HTML tables of the different alexandria permissions for debugging purposes. To run the script you need to have node installed.

```bash
node dump-alexandria-permissions.js ../../django/kt_gr/config/alexandria_core.json
```

Then open the permissions.html in your browser.
