Derived from datasets within `../datasets` as follows:

``bash
mkdir -p /tmp/test/
cp -r ../datasets /tmp/test/lhs
cp -r ../datasets /tmp/test/rhs
rm -rf /tmp/test/lhs/he
rm -rf /tmp/test/rhs/people
dtool create changed /tmp/test/lhs
echo "content" > /tmp/test/file.txt
dtool add item /tmp/test/file.txt /tmp/test/lhs/changed
cp -r /tmp/test/lhs/changed /tmp/test/rhs/
dtool freeze /tmp/test/rhs/changed
cp -r /tmp/test/lhs .
cp -r /tmp/test/rhs .
```