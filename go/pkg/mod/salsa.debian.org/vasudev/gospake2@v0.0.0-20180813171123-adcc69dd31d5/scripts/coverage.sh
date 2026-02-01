#!/bin/sh

set -eu

COVERAGE_DIR="${COVERAGE_DIR:-coverage}"
PKG_LIST=$(go list ./... | grep -v /cmd/ | grep -v /groups/)


[ -d "$COVERAGE_DIR" ] || mkdir -p "$COVERAGE_DIR"

for package in ${PKG_LIST}; do
    go test -covermode=count -coverprofile "${COVERAGE_DIR}/${package##*/}.cov" "$package" ;
done ;


# Merge the coverage profile files
echo 'mode: count' > "${COVERAGE_DIR}"/coverage.cov ;
tail -q -n +2 "${COVERAGE_DIR}"/*.cov >> "${COVERAGE_DIR}"/coverage.cov ;

# Display the global code coverage
go tool cover -func="${COVERAGE_DIR}"/coverage.cov ;
go tool cover -html="${COVERAGE_DIR}"/coverage.cov -o coverage.html ;

rm -rf "${COVERAGE_DIR}"
