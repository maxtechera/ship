# Credentials Extensions

Drop additional `*.yml` files here (or in `$SHIP_EXTENSIONS_DIR`) to add workspace-specific checks to the credentials registry.

Each extension file follows the same schema as `registry/core.yml`. Example:

```yaml
version: 1
checks:
  - id: my_service
    category: api-token
    detect:
      env: MY_SERVICE_TOKEN
      token_file: .my_service_token
      whoami:
        url: https://api.my-service.com/me
        auth: "header:Bearer"
    fix:
      summary: "Paste new My Service token"
      template: "echo 'mst_...' > {cred_dir}/.my_service_token && chmod 600 {cred_dir}/.my_service_token"
```

See `docs/extensions/kumello.yml.example` in the repo root for a working sample.

Extension files merge *after* the core registry — you can override a core check by redeclaring its `id`.
