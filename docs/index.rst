NextGenVol IBKR Reports
==============================================
NextGenVol IBKR Reports pulls trade and position data from Interactive Brokers and
turns it into reports. It covers two data sources:

* **Flex Web Service** — annual/periodic Flex Query reports, fetched either through
  ``ib_async``'s ``FlexReport`` or through :mod:`ngv_reports_ibkr.flex_client`, which
  talks to the Flex Web Service (version 3) directly and supports custom start/end
  dates, retry with exponential backoff, and typed error handling.
* **TWS realtime trades** — trade objects from the TWS API, flattened into DataFrames
  by :mod:`ngv_reports_ibkr.expand_contract_columns`.

Both sources are validated with `pandera <https://pandera.readthedocs.io/>`_ schemas
(:mod:`ngv_reports_ibkr.schemas`) and can be merged into a single deduplicated
DataFrame keyed on execution ID by :mod:`ngv_reports_ibkr.unified_df`.

Installation and setup instructions live in the project
`README <https://github.com/westonplatter/ngv_reports_ibkr#readme>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

API Reference
-------------

.. toctree::
   :maxdepth: 2

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
