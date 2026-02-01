#!/bin/sh

set -eu

# Get golang.org/x/crypto/hkdf
go get -u golang.org/x/crypto/hkdf

# get golint
go get -u golang.org/x/lint/golint
