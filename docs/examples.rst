********
Examples
********

The following code block will be tested and raise an error:

.. code-block:: python

    one = 1
    assert(one == 2)


The following code block will be tested and will not raise an error:

.. code-block:: python

    one = 1
    assert(one == 1)

The following code block will **NOT** be tested:

.. 
    no-test

.. code-block:: python

    one = 1
    assert(one == 2)

The block above is not tested because it has the *no-test* comment before it. If you were to look at the raw RST of the code-block above, it would look like:

.. code-block:: text

    .. 
        no-test

    .. code-block...
