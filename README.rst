
README
******

One-way synchronisation for data management command line tool dtool.


Overview
========

The ``dtool-sync`` python package provides a command line interface
for synchronization between different dataset base URIs.

It introduces ``dtool sync`` for batch comparison and transfer of datasets from
one base URI to the other.


Usage
=====

Use the `--dry-run` or `-n` option to compare datasets at two different base
URIs:

::

   $ dtool sync --dry-run lhs rhs
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
followed by datasets that are present at both URIs, but differ by metadata
or their frozen status. A common case for differing datasets is an interrupted
transfer. In such a case, the source dataset is has been frozen before, but its
partial copy at the destination is still marked as a proto dataset.
Eventually, datasets present at the left hand side URI, but missing at
the right hand side URI are shown. Note that datasets present at rhs
but missing at lhs are not shown. To identify those, invert the
comparison’s direction.

To actually sync from ``lhs`` to ``rhs``, use

::

   $ dtool sync lhs rhs
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

``dtool sync`` will raise an error if the transfer fails at a single dataset.
To ignore a single failure and continue with the transfer, use the
``--ignore-errors`` flag.

Use ``-verbose`` or *-v* to show more metadata in the output:

::

   $ dtool sync --dry-run -v lhs rhs
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

To print the comparison results in JSON, use ``--json`` or ``-j``.

::

   $ dtool sync --dry-run -j lhs rhs
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

As above, use ``--verbose`` or ``-v`` to show more metadata in the
JSON-formatted output. In this case, ``equal`` and ``changed`` are
shown as lists of tuples of datasets.

::

   $ dtool sync --dry-run -jv lhs rhs
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


To compare against the index of a configured lookup server, use the dummy
``lookup://`` scheme, i.e.

::

  dtool sync --dry-run -jv file://lhs lookup://rhs

To compare against one base URI, but actually transfer datasets to another,
just specify three base URIs in the order `source`, `target for comparison`,
and `target for transfer`, i.e.

::

  dtool sync --dry-run -jv file://source lookup://server s3://target

Installation
============

To install the dtool-sync package,

.. code:: bash

   cd dtool-sync
   python setup.py install
