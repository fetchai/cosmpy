.. cosmpy documentation master file, created by
   sphinx-quickstart on Wed Sep  1 17:31:48 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to cosmpy's documentation!
==================================

|Checks amd Tests|

A python library for interacting with cosmos based blockchain networks

Installing
----------

To install the project use:

::

    pip3 install cosmpy

Getting started
---------------

Below is a simple example using the ``SigningCosmWasmClient`` and the
``RestClient`` channel.

::

    from cosmpy.clients.signing_cosmwasm_client import SigningCosmWasmClient
    from cosmpy.common.rest_client import RestClient

    channel = RestClient("http://<rest endpoint addres>")
    client = SigningCosmWasmClient(private_key, channel, "<chain id>")

    res = client.get_balance(client.address, "stake")
    print(f"Balance: {res.balance.amount} {res.balance.denom}")

Extra Resources
---------------

-  `Github Repo <https://github.com/fetchai/cosmpy>`__
-  `Bug Reports <https://github.com/fetchai/cosmpy/issues>`__
-  `Discussions <https://github.com/fetchai/cosmpy/discussions>`__

.. |Checks amd Tests| image:: https://github.com/fetchai/cosmpy/actions/workflows/workflow.yml/badge.svg
   :target: https://github.com/fetchai/cosmpy/actions/workflows/workflow.yml


.. toctree::
   :maxdepth: 8
   :caption: Contents:

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
