
#!/usr/bin/env bash

# Default to ".env" file.
# You can also pass an environment suffix (e.g. "dev", "prod"),
# and it will load ".env.dev" or ".env.prod" instead.
#
# Examples:
#   ./init.sh         # loads .env
#   ./init.sh dev     # loads .env.dev
#   ./init.sh prod    # loads .env.prod

ENV_FILE=".env"
if [ -n "$1" ]; then
  ENV_FILE=".env.$1"
fi

if [ ! -f "$ENV_FILE" ]; then
  echo "File $ENV_FILE not found!"
  exit 1
fi

echo "Loading environment variables from $ENV_FILE"

# Export every non-comment, non-empty line as-is (no key name validation)
grep -v '^#' "$ENV_FILE" | sed '/^\s*$/d' | while IFS='=' read -r key value; do
  export "$key=$value"
done

echo "Environment variables from $ENV_FILE have been loaded."
