#!/usr/bin/env sh
# Make the repository's versioned hooks active for this local checkout.
set -eu

git config core.hooksPath .githooks
printf '%s\n' 'Enabled repository Git hooks from .githooks.'
