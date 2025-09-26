# Jotsu

This is the official Jotsu Python SDK and cli.

## Command Line Interface (CLI)

### Getting Started
Navigate to https://my.jotsu.com/api-keys and create an API key.

Copy the key and create a `.env` file, such as:
```shell
JOTSU_ACCOUNT_ID=<your-account-id>
JOTSU_API_KEY=<your-api-key-here>
```

Replacing `<your-account-id>` and `<your-api-key-here>` with your Jotsu account id and the copied key (without the brackets), respectively.

```shell
pip install jotsu
```

Verify everything is working correctly via:
```shell
jotsu whoami
```

## Contributing

```shell
pip install -e .
```


