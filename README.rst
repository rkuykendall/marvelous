marvelous - Marvel API wrapper for python 3
===========================================

.. image:: https://travis-ci.org/rkuykendall/marvelous.svg?branch=master
    :target: https://travis-ci.org/rkuykendall/marvelous

.. image:: https://codecov.io/gh/rkuykendall/marvelous/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/rkuykendall/marvelous

- `Code on Github <https://github.com/rkuykendall/marvelous>`_
- `Published on PyPi <https://pypi.python.org/pypi/marvelous>`_
- `Read the project documentation <http://marvelous.readthedocs.io/en/latest/>`_
- `Marvel API documentation <https://developer.marvel.com/docs>`_

**To install:**

.. code-block:: bash

    pip install marvelous

**Example Usage:**

.. code-block:: python

    import marvelous

    # Your own config file to keep your private key local and secret
    from config import public_key, private_key

    # Authenticate with Marvel, with keys I got from http://developer.marvel.com/
    m = marvelous.api(public_key, private_key)

    # Get all comics from this week, sorted alphabetically by title
    pulls = sorted(m.comics({
        'format': "comic",
        'formatType': "comic",
        'noVariants': True,
        'dateDescriptor': "thisWeek",
        'limit': 100}),
        key=lambda comic: comic.title)

    for comic in pulls:
        # Write a line to the file with the name of the issue, and the
        # id of the series
        print('{} (series #{})'.format(comic.title, comic.series.id))

`Output available in full documentation <http://marvelous.readthedocs.io/en/latest/>`_


Contributing
------------

- To run the test suite, run `python -m nose` in this folder
- When running a new test for the first time, set the environment variables
  ``PUBLIC_KEY`` and ``PRIVATE_KEY`` to any Marel API keys. The result will be
  stored in the `tests/testing_mock.sqlite` database without your keys.


**To release:**

- Update version number
- Create tag on Github
- Wait for Travis to publish
