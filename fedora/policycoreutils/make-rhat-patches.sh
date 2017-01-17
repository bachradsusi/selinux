#!/bin/bash

POLICYCOREUTILS_VERSION=2.4
SEPOLGEN_VERSION=1.2.2
BRANCH=master

REBASEDIR=`mktemp -d rebase.XXXXXX`
pushd $REBASEDIR

git clone git@github.com:fedora-selinux/selinux.git
pushd selinux; git checkout $BRANCH; COMMIT=`git rev-parse --verify HEAD`; popd

# prepare policycoreutils-rhat.patch
tar xfz ../policycoreutils-$POLICYCOREUTILS_VERSION.tar.gz
pushd policycoreutils-$POLICYCOREUTILS_VERSION

git init; git add .; git commit -m "init"
cp -r ../selinux/policycoreutils/* .
git add -A .

git diff --cached --src-prefix=a/policycoreutils-$POLICYCOREUTILS_VERSION/ --dst-prefix=b/policycoreutils-$POLICYCOREUTILS_VERSION/ > ../../policycoreutils-rhat.patch

popd

#prepare sepolgen-rhat.patch
tar xfz ../sepolgen-$SEPOLGEN_VERSION.tar.gz
pushd sepolgen-$SEPOLGEN_VERSION

git init; git add .; git commit -m "init"
cp -r ../selinux/sepolgen/* .
git add -A .

git diff --cached --src-prefix=a/sepolgen-$SEPOLGEN_VERSION/ --dst-prefix=b/sepolgen-$SEPOLGEN_VERSION/ > ../../sepolgen-rhat.patch

popd

popd
# echo rm -rf $REBASEDIR

echo policycoreutils-rhat.patch and sepolgen-rhat.patch created from https://github.com/fedora-selinux/selinux/commit/$COMMIT
