# Jotsu

This is the official Jotsu Python SDK and cli.

## Command Line Interface (CLI)

### Getting Started
Navigate to https://my.jotsu.com/api-keys and create an API key.

Copy the key and create a `.env` file, such as:
```shell
JOTSU_API_KEY=<your-api-key-here>
```

Replacing `<your-api-key-here>` with the copied key (without the brackets).

```shell
pip install jotsu
```

Verify everything is working correctly via:
```shell
jotsu whoami
```

## Contributing

```shell
brew install openapi-generator   # or npm install @openapitools/openapi-generator-cli -g
pip install -e .
```
