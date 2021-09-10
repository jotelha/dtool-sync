
README
******

One-way synchronisation for data management command line tool dtool.


Overview
========

The ``dtool-sync`` python package provides a command line interface
for synchronization between different dataset base URIs.

It introduces two new subcommands, ``dtool compare`` for comparing two
base URIs and ``dtool sync`` for actually transferring datasets from
one base URI to the other.


Usage
=====

Compare datasets at two different base URIs:

::

   $ dtool compare all lhs rhs
   Datasets equal on source and target:
   lion
     file://path/to/lhs/lion
   she
     file://path/to/lhs/she
   cat
     file://path/to/lhs/cat
   Datasets changed from source to target:
   changed
     file://path/to/lhs/changed
   Datasets missing on target:
   people
     file://path/to/lhs/people

Datasets identified as equal by comparing their metadata appear first,
followed by datasets that are present at both URIs, but have changed.
A common case for differing datasets is an interrupted transfer. In
such a case, the source dataset is has been frozen before, but its
partial copy at the destination is still marked as a proto dataset.
Eventually, datasets present at the left hand side URI, but missing at
the right hand side URI are shown. Note that datasets present at rhs
but missing at lhs are not shown. To identify those, invert the
comparison’s direction.

To actually sync from ``lhs`` to ``rhs``, use

::

   $ dtool sync all lhs rhs
   Datasets equal on source and target:
   lion
     file://path/to/lhs/lion
   she
     file://path/to/lhs/she
   cat
     file://path/to/lhs/cat
   Datasets changed from source to target:
   changed
     file://path/to/lhs/changed
   Datasets missing on target:
   people
     file://path/to/lhs/people
   Resume copying of changed datasets, presuming their transfer had been interrupted in an earlier attempt.
   Dataset copied to:
   file://path/to/rhs/changed
   Copy missing datasets.
   Dataset copied to:
   file://path/to/rhs/people

Datasets already partially present at ``rhs`` are transferred first,
then missing datasets. Again, this only syncs one way from ``lhs`` to
``rhs``.

Use ``-verbose`` or *-v* to show more metadata in the output:

::

   $ dtool compare all -v lhs rhs
   Datasets equal on source and target:
   lion
     file://path/to/lhs/lion
     jotelha  2021-09-05  065d9fe0-9e41-4add-8a55-577dbcfe2149
   she
     file://path/to/lhs/she
     jotelha  2021-09-05  9ee101a4-7d1a-45c0-8955-da779398a5ed
   cat
     file://path/to/lhs/cat
     jotelha  2021-09-05  c2249963-6459-4901-8263-85610a7a2ac9
   Datasets changed from source to target:
   changed
     file://path/to/lhs/changed
     jotelha  2021-09-05  af16c00d-f60d-41ce-83c6-2a7d9c5e1b0d
   Datasets missing on target:
   people
     file://path/to/lhs/people
     jotelha  2021-09-05  534792bd-d102-4efc-bc11-6af743959704

To put emphasis on the UUID instead of the name in the output of
``compare``, use ``--uuid`` or *-u`*…

::

   $ dtool compare all -u lhs rhs
   Datasets equal on source and target:
   065d9fe0-9e41-4add-8a55-577dbcfe2149
     file://path/to/lhs/lion
   9ee101a4-7d1a-45c0-8955-da779398a5ed
     file://path/to/lhs/she
   c2249963-6459-4901-8263-85610a7a2ac9
     file://path/to/lhs/cat
   Datasets changed from source to target:
   af16c00d-f60d-41ce-83c6-2a7d9c5e1b0d
     file://path/to/lhs/changed
   Datasets missing on target:
   534792bd-d102-4efc-bc11-6af743959704
     file://path/to/lhs/people

… and combine with ``-v`` as you please:

::

   $ dtool compare all -uv lhs rhs
   Datasets equal on source and target:
   065d9fe0-9e41-4add-8a55-577dbcfe2149
     file://path/to/lhs/lion
     jotelha  2021-09-05  lion
   9ee101a4-7d1a-45c0-8955-da779398a5ed
     file://path/to/lhs/she
     jotelha  2021-09-05  she
   c2249963-6459-4901-8263-85610a7a2ac9
     file://path/to/lhs/cat
     jotelha  2021-09-05  cat
   Datasets changed from source to target:
   af16c00d-f60d-41ce-83c6-2a7d9c5e1b0d
     file://path/to/lhs/changed
     jotelha  2021-09-05  changed
   Datasets missing on target:
   534792bd-d102-4efc-bc11-6af743959704
     file://path/to/lhs/people
     jotelha  2021-09-05  people

Instead of ``all``, just list ``changed``, ``equal`` or ``missing``
datasets and use ``--quiet`` or -q` to only identify the datasets by
name…

::

   $ dtool compare changed -q lhs rhs
   file://path/to/lhs/changed

… JSON-formatted …

::

   $ dtool compare missing -jq lhs rhs
   [
       "534792bd-d102-4efc-bc11-6af743959704"
   ]

… or by UUID:

::

   $ dtool compare equal -qu lhs rhs
   065d9fe0-9e41-4add-8a55-577dbcfe2149
   9ee101a4-7d1a-45c0-8955-da779398a5ed
   c2249963-6459-4901-8263-85610a7a2ac9

To print the comparison results in JSON, use ``--json`` or ``-j``.
With the ``all`` command, the output is categorized into a dict with
keys ``equal``, ``changed``, and ``missing``.

::

   $ dtool compare all -j lhs rhs
   {
       "equal": [
           {
               "name": "lion",
               "uuid": "065d9fe0-9e41-4add-8a55-577dbcfe2149",
               "creator_username": "jotelha",
               "frozen_at": "2021-09-05"
           },
           {
               "name": "she",
               "uuid": "9ee101a4-7d1a-45c0-8955-da779398a5ed",
               "creator_username": "jotelha",
               "frozen_at": "2021-09-05"
           },
           {
               "name": "cat",
               "uuid": "c2249963-6459-4901-8263-85610a7a2ac9",
               "creator_username": "jotelha",
               "frozen_at": "2021-09-05"
           }
       ],
       "changed": [
           {
               "name": "changed",
               "uuid": "af16c00d-f60d-41ce-83c6-2a7d9c5e1b0d",
               "creator_username": "jotelha",
               "frozen_at": "2021-09-05"
           }
       ],
       "missing": [
           {
               "name": "people",
               "uuid": "534792bd-d102-4efc-bc11-6af743959704",
               "creator_username": "jotelha",
               "frozen_at": "2021-09-05"
           }
       ]
   }

Again, ``--quiet`` or ``-q`` lists only the names (or UUIDs in
connection with ``-u``).

::

   $ dtool compare all -jq lhs rhs
   {
       "equal": [
           "065d9fe0-9e41-4add-8a55-577dbcfe2149",
           "9ee101a4-7d1a-45c0-8955-da779398a5ed",
           "c2249963-6459-4901-8263-85610a7a2ac9"
       ],
       "changed": [
           "af16c00d-f60d-41ce-83c6-2a7d9c5e1b0d"
       ],
       "missing": [
           "534792bd-d102-4efc-bc11-6af743959704"
       ]
   }

As above, use ``--verbose`` or ``-v`` to show more metadata in the
JSON-formatted output. In this case, ``equal`` and ``changed`` are
shown as lists of tuples of datasets.

::

   $ dtool compare all -jv lhs rhs
   {
       "equal": [
           [
               {
                   "name": "lion",
                   "uuid": "065d9fe0-9e41-4add-8a55-577dbcfe2149",
                   "creator_username": "jotelha",
                   "uri": "file://path/to/lhs/lion",
                   "frozen_at": "2021-09-05"
               },
               {
                   "name": "lion",
                   "uuid": "065d9fe0-9e41-4add-8a55-577dbcfe2149",
                   "creator_username": "jotelha",
                   "uri": "file://path/to/rhs/lion",
                   "frozen_at": "2021-09-05"
               }
           ],
           [
               {
                   "name": "she",
                   "uuid": "9ee101a4-7d1a-45c0-8955-da779398a5ed",
                   "creator_username": "jotelha",
                   "uri": "file://path/to/lhs/she",
                   "frozen_at": "2021-09-05"
               },
               {
                   "name": "she",
                   "uuid": "9ee101a4-7d1a-45c0-8955-da779398a5ed",
                   "creator_username": "jotelha",
                   "uri": "file://path/to/rhs/she",
                   "frozen_at": "2021-09-05"
               }
           ],
           [
               {
                   "name": "cat",
                   "uuid": "c2249963-6459-4901-8263-85610a7a2ac9",
                   "creator_username": "jotelha",
                   "uri": "file://path/to/lhs/cat",
                   "frozen_at": "2021-09-05"
               },
               {
                   "name": "cat",
                   "uuid": "c2249963-6459-4901-8263-85610a7a2ac9",
                   "creator_username": "jotelha",
                   "uri": "file://path/to/rhs/cat",
                   "frozen_at": "2021-09-05"
               }
           ]
       ],
       "changed": [
           [
               {
                   "name": "changed",
                   "uuid": "af16c00d-f60d-41ce-83c6-2a7d9c5e1b0d",
                   "creator_username": "jotelha",
                   "uri": "file://path/to/lhs/changed",
                   "frozen_at": "2021-09-05"
               },
               {
                   "name": "*changed",
                   "uuid": "af16c00d-f60d-41ce-83c6-2a7d9c5e1b0d",
                   "creator_username": "jotelha",
                   "uri": "file://path/to/rhs/changed"
               }
           ]
       ],
       "missing": [
           {
               "name": "people",
               "uuid": "534792bd-d102-4efc-bc11-6af743959704",
               "creator_username": "jotelha",
               "uri": "file://path/to/lhs/people",
               "frozen_at": "2021-09-05"
           }
       ]
   }

Direct use of the ``equal``, ``changed``, and ``missing`` subcommand
makes such upper-level categorization obsolete. The output is a list
of datasets:

::

   $ dtool compare changed -j lhs rhs
   [
       {
           "name": "changed",
           "uuid": "af16c00d-f60d-41ce-83c6-2a7d9c5e1b0d",
           "creator_username": "jotelha",
           "frozen_at": "2021-09-05"
       }
   ]

::

   $ dtool compare changed -jv lhs rhs
   [
       [
           {
               "name": "changed",
               "uuid": "af16c00d-f60d-41ce-83c6-2a7d9c5e1b0d",
               "creator_username": "jotelha",
               "uri": "file://path/to/lhs/changed",
               "frozen_at": "2021-09-05"
           },
           {
               "name": "*changed",
               "uuid": "af16c00d-f60d-41ce-83c6-2a7d9c5e1b0d",
               "creator_username": "jotelha",
               "uri": "file://path/to/rhs/changed"
           }
       ]
   ]

The ``--raw`` or ``-r`` flag displays metadata (in particular
timestamps) as stored without any conversion reformatting for pretty
output:

::

   $ dtool compare all -rv lhs rhs
   Datasets equal on source and target:
   lion
     file://path/to/lhs/lion
     jotelha  1630851896.375779  065d9fe0-9e41-4add-8a55-577dbcfe2149
   she
     file://path/to/lhs/she
     jotelha  1630851892.800604  9ee101a4-7d1a-45c0-8955-da779398a5ed
   cat
     file://path/to/lhs/cat
     jotelha  1630851894.593098  c2249963-6459-4901-8263-85610a7a2ac9
   Datasets changed from source to target:
   changed
     file://path/to/lhs/changed
     jotelha  1630862808.395145  af16c00d-f60d-41ce-83c6-2a7d9c5e1b0d
   Datasets missing on target:
   people
     file://path/to/lhs/people
     jotelha  1630851899.345241  534792bd-d102-4efc-bc11-6af743959704


Installation
============

To install the dtool-sync package,

.. code:: bash

   cd dtool-sync
   python setup.py install
