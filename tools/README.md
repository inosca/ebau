# camac-ng tools

## Upload RSTA Templates

Command to distribute RSTA template files

```bash
yarn upload-rsta-templates
```

| Argument     | Description                                                                                    | Default                                                        |
| ------------ | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `pattern`    | Glob pattern of file(s) to upload                                                              | `"../document-merge-service/kt_bern/rsta_templates/\*.docx"`   |
| `groups`     | Comma-separated list of groups to upload to (your token has to be valid for all of them!)      | Preconfigured list of RSTA admin groups for dev and production |
| `host`       | Base path to upload to                                                                         | `"http://camac-ng.local"`                                      |
| `token`      | The OIDC token to authorize                                                                    | `process.env.TOKEN`                                            |
| `skip-patch` | Skip all updates, only upload new templates                                                    | `false`                                                        |
| `delete`     | Delete all existing templates that have match the RSTA prefixes: `/^(bpv\|nhhe\|nhsb\|rsta)_/` | `false`                                                        |
| `dry-run`    | Show what would be done without actually doing requests                                        | `false`                                                        |
