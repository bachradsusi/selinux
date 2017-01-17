#!/bin/bash

LIBSEMANAGE_VERSION=2.4
BRANCH=master

REBASEDIR=`mktemp -d rebase.XXXXXX`
pushd $REBASEDIR

git clone git@github.com:fedora-selinux/selinux.git
pushd selinux; git checkout $BRANCH; COMMIT=`git rev-parse --verify HEAD`; popd

# prepare libsemanage-rhat.patch
tar xfz ../libsemanage-$LIBSEMANAGE_VERSION.tar.gz
pushd libsemanage-$LIBSEMANAGE_VERSION

git init; git add .; git commit -m "init"
cp -r ../selinux/libsemanage/* .
git add -A .

git diff --cached --src-prefix=libsemanage-$LIBSEMANAGE_VERSION/ --dst-prefix=libsemanage-$LIBSEMANAGE_VERSION/ > ../../libsemanage-rhat.patch

popd

popd
# echo rm -rf $REBASEDIR

echo libsemanage-rhat.patch created from https://github.com/fedora-selinux/selinux/commit/$COMMIT
