README
======

One-way synchronisation for data management command line tool dtool.

Overview
--------

The ``dtool-sync`` python package provides a command line interface for
synchronization between different dataset base URIs.

It introduces two new subcommands, ``dtool compare`` for comparing
two base URIs and ``dtool sync`` for actually transferring datasets
from one base URI to the other.


Usage
-----

Compare datasets at two different base URIs:

.. ansi-block::

    $ dtool compare all lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_lhs_rhs.out" %}{% endfilter %}

Datasets identified as equal by comparing their metadata appear first,
followed by datasets that are present at both URIs, but have changed.
A common case for differing datasets is an interrupted transfer.
In such a case, the source dataset is has been frozen before, but its
partial copy at the destination is still marked as a proto dataset.
Eventually, datasets present at the left hand side URI, but missing
at the right hand side URI are shown. Note that datasets present at
rhs but missing at lhs are not shown. To identify those, invert the
comparison's direction. 

To actually sync from ``lhs`` to ``rhs``, use

.. ansi-block::

    $ dtool sync all lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_sync_all_lhs_rhs.out" %}{% endfilter %}

Datasets already partially present at ``rhs`` are transferred first, then missing datasets.
Again, this only syncs one way from ``lhs`` to ``rhs``.

Use ``-verbose`` or `-v` to show more metadata in the output:
  
.. ansi-block::

    $ dtool compare all -v lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_v_lhs_rhs.out" %}{% endfilter %}

To put emphasis on the UUID instead of the name in the output of ``compare``, use ``--uuid`` or `-u``...

.. ansi-block::

    $ dtool compare all -u lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_u_lhs_rhs.out" %}{% endfilter %}

... and combine with ``-v`` as you please:

.. ansi-block::

    $ dtool compare all -uv lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_uv_lhs_rhs.out" %}{% endfilter %}

Instead of ``all``, just list ``changed``, ``equal`` or ``missing`` datasets and use 
``--quiet`` or -q` to only identify the datasets by name...

.. ansi-block::

    $ dtool compare changed -q lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_changed_q_lhs_rhs.out" %}{% endfilter %}

... JSON-formatted ...

.. ansi-block::

    $ dtool compare missing -jq lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_missing_jq_lhs_rhs.out" %}{% endfilter %}

... or by UUID:

.. ansi-block::

    $ dtool compare equal -qu lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_equal_qu_lhs_rhs.out" %}{% endfilter %}


To print the comparison results in JSON, use ``--json`` or ``-j``. With the ``all`` command, the 
output is categorized into a dict with keys ``equal``, ``changed``, and ``missing``.

.. ansi-block::

    $ dtool compare all -j lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_j_lhs_rhs.out" %}{% endfilter %}


Again, ``--quiet`` or ``-q`` lists only the names (or UUIDs in connection with ``-u``).

.. ansi-block::

    $ dtool compare all -jq lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_jq_lhs_rhs.out" %}{% endfilter %}


As above, use ``--verbose`` or ``-v`` to show more metadata in the JSON-formatted output.
In this case, ``equal`` and ``changed`` are shown as lists of tuples of datasets.

.. ansi-block::

    $ dtool compare all -jv lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_jv_lhs_rhs.out" %}{% endfilter %}

Direct use of the ``equal``, ``changed``, and ``missing`` subcommand makes such upper-level categorization
obsolete. The output is a list of datasets:

.. ansi-block::

    $ dtool compare changed -j lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_changed_j_lhs_rhs.out" %}{% endfilter %}


.. ansi-block::

    $ dtool compare changed -jv lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_changed_jv_lhs_rhs.out" %}{% endfilter %}


The ``--raw`` or ``-r`` flag displays metadata (in particular timestamps) as stored without any conversion 
reformatting for pretty output:

.. ansi-block::

    $ dtool compare all -rv lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_rv_lhs_rhs.out" %}{% endfilter %}


Installation
------------

To install the dtool-sync package,

.. code-block:: bash

    cd dtool-sync
    python setup.py install
