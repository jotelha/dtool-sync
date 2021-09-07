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

    $ dtool compare all -v lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_v_lhs_rhs.out" %}{% endfilter %}

Datasets identified as equal by comparing their metadata appear first,
followed by datasets that are present at both URIs, but have changed.
A common case for differing datasets is an interrupted transfer.
In such a case, the source dataset is has been frozen before, but its
partial copy at the destination is still marked as a proto dataset.
Eventually, datasets present at the left hand side URI, but missing
at the right hand side URI are shown. Note that datasets present at
rhs but missing at lhs are not shown. To identify those, invert the
comparison's direction.

.. ansi-block::

    $ dtool sync all lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_sync_all_lhs_rhs.out" %}{% endfilter %}

.. ansi-block::

    $ dtool compare all -uv lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_uv_lhs_rhs.out" %}{% endfilter %}

.. ansi-block::

    $ dtool compare all -j lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_j_lhs_rhs.out" %}{% endfilter %}

.. ansi-block::

    $ dtool compare changed -j lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_changed_j_lhs_rhs.out" %}{% endfilter %}

.. ansi-block::

    $ dtool compare changed -jv lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_changed_jv_lhs_rhs.out" %}{% endfilter %}

.. ansi-block::

    $ dtool compare all -u lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_u_lhs_rhs.out" %}{% endfilter %}

.. ansi-block::

    $ dtool compare changed -q lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_changed_q_lhs_rhs.out" %}{% endfilter %}

.. ansi-block::

    $ dtool compare missing -jq lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_missing_jq_lhs_rhs.out" %}{% endfilter %}

.. ansi-block::

    $ dtool compare all -jq lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_jq_lhs_rhs.out" %}{% endfilter %}

.. ansi-block::

    $ dtool compare all lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_lhs_rhs.out" %}{% endfilter %}

.. ansi-block::

    $ dtool compare all -jv lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_jv_lhs_rhs.out" %}{% endfilter %}


.. ansi-block::

    $ dtool compare equal -qu lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_equal_qu_lhs_rhs.out" %}{% endfilter %}


.. ansi-block::

    $ dtool compare all -rv lhs rhs
    {% filter indent(4) %}{% include_raw "output/dtool_compare_all_rv_lhs_rhs.out" %}{% endfilter %}


Installation
------------

To install the dtool-sync package,

.. code-block:: bash

    cd dtool-sync
    python setup.py install
