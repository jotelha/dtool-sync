README
======

One-way synchronisation for data management command line tool dtool.

Overview
--------

The ``dtool-sync`` python package provides a command line interface for
synchronization between different dataset base URIs.

It makes use of `click <https://github.com/pallets/click>`_ and `click-plugins
<https://github.com/click-contrib/click-plugins>`_.

Usage
-----

Compare datasets at two different base URIs by UUID:

```console
$ dtool sync diff -q /tmp/test/lhs /tmp/test/rhs
--- /tmp/test/lhs
+++ /tmp/test/rhs
@@ -1,4 +1,4 @@
 0b5f7c56-5f7e-43de-9b16-bd6f7ac7da12
+33a30c8d-60c2-44ac-8ade-abe99a7e2f92
 5cb6d8bb-255b-4ca5-a445-c1f8121c5333
-9d14c3e3-2c87-4bff-9e17-3c51f5f535a0
 cc6519a9-7862-4b47-91d2-105d4ae64512
```

Compare by name and UUID:

```console
$ dtool sync diff /tmp/test/lhs /tmp/test/rhs
--- /tmp/test/lhs
+++ /tmp/test/rhs
@@ -1,8 +1,8 @@
 she
   0b5f7c56-5f7e-43de-9b16-bd6f7ac7da12
+he
+  33a30c8d-60c2-44ac-8ade-abe99a7e2f92
 lion
   5cb6d8bb-255b-4ca5-a445-c1f8121c5333
-people
-  9d14c3e3-2c87-4bff-9e17-3c51f5f535a0
 cat
   cc6519a9-7862-4b47-91d2-105d4ae64512
```

Compare by UUIDs formatted as JSON list:

```console
dtool sync diff -qj /tmp/test/lhs /tmp/test/rhs
--- /tmp/test/lhs
+++ /tmp/test/rhs
@@ -1,6 +1,6 @@
 [
     "0b5f7c56-5f7e-43de-9b16-bd6f7ac7da12",
+    "33a30c8d-60c2-44ac-8ade-abe99a7e2f92",
     "5cb6d8bb-255b-4ca5-a445-c1f8121c5333",
-    "9d14c3e3-2c87-4bff-9e17-3c51f5f535a0",
     "cc6519a9-7862-4b47-91d2-105d4ae64512"
 ]
```

Installation
------------

To install the dtool-sync package,

.. code-block:: bash

    cd dtool-sync
    python setup.py install
