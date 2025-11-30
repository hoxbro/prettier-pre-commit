# Prettier pre-commit

For prettier: see https://github.com/prettier/prettier

For pre-commit: see https://github.com/pre-commit/pre-commit

## Using prettier with pre-commit

Add this to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/hoxbro/prettier-pre-commit
  rev: v3.7.3
  hooks:
    - id: prettier
      types_or: [css, javascript] # Optional
```

By default, all files are passed to `prettier`, if you want to limit the
file list, adjust `types` / `types_or` / `files`.
