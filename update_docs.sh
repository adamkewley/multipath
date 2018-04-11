#!/usr/bin/env bash

TMP_DIR=$(mktemp -d)

pushd docs

make clean
sphinx-apidoc -o source ..
make html

cp cp -r build/html/* ${TMP_DIR}

popd docs

git checkout gh-pages
rm -rf *
touch .nojekyll
cp -r ${TMP_DIR}/* .
