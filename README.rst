marvelous
=========

Marvel API python wrapper.
[Read the project documentation](http://marvelous.readthedocs.org/en/latest/)

Contributing
------------

- To run the test suite, run `python -m nose` in the `tests` folder
- When running a new test for the first time, set the environment variables
  `PUBLIC_KEY` and `PRIVATE_KEY` to any Marel API keys. The result will be
  stored in the `testing_mock` database without your keys.

Examples
--------

This is a script which can be run at the beginning on the week to generate a
complete Marvel pull list, excluding any series the user doesn't want.

.. code-block:: python

    import os
    import marvelous

    # Your own config file to keep your private key local and secret
    from config import public_key, private_key

    # All the series IDs of comics I'm not interested in reading
    # I pull these out of the resulting pulls.txt file, then rerun this script
    IGNORE = set([
        19709, 20256, 19379, 19062, 19486, 19242, 19371, 19210, 20930, 21328,
        20834, 18826, 20933, 20365, 20928, 21129, 20786, 21402, 21018
    ])

    # Authenticate with Marvel, with keys I got from http://developer.marvel.com/
    m = marvelous.api(public_key, private_key)

    # Get all comics from this week, sorted alphabetically by title
    # Uses the same API parameters as listed in the official API documentation
    pulls = sorted(m.comics({
        'format': "comic",
        'formatType': "comic",
        'noVariants': True,
        'dateDescriptor': "thisWeek",
        'limit': 100}),
        key=lambda comic: comic.title)

    # Grab the sale date of any of the comics for the current week
    week = pulls[0].dates.on_sale.strftime('%m/%d')

    print("New comics for the week of {}:".format(week))
    # Check each comic that came out this week
    for comic in pulls:
        # If this series isn't in my ignore list
        if comic.series.id not in IGNORE:
            # Write a line to the file with the name of the issue, and the
            # id of the series incase I want to add it to my ignore list
            print('- {} (series #{})'.format(comic.title, comic.series.id))


Example output::

    New comics for the week of 11/09:
    - All-New X-Men (2015) #15 (series #20622)
    - Amazing Spider-Man: Renew Your Vows (2016) #1 (series #22545)
    - Black Panther: World of Wakanda (2016) #1 (series #22549)
    - Captain America: Steve Rogers (2016) #7 (series #21098)
    - Daredevil (2015) #13 (series #20780)
    - Dark Tower: The Drawing of the Three - The Sailor (2016) #2 (series #19377)
    - Deadpool: Back in Black (2016) #3 (series #21489)
    - Doctor Strange And The Sorcerers Supreme (2016) #2 (series #22560)
    - Gwenpool (2016) #8 (series #21490)
    - Han Solo (2016) #5 (series #19711)
    - Invincible Iron Man (2016) #1 (series #22928)
    - Max Ride: Final Flight (2016) #3 (series #22197)
    - Mosaic (2016) #2 (series #20818)
    - Ms. Marvel (2015) #13 (series #20615)
    - Old Man Logan (2016) #13 (series #20617)
    - Power Man and Iron Fist (2016) #10 (series #21122)
    - Prowler (2016) #2 (series #22535)
    - Solo (2016) #2 (series #22441)
    - Spider-Gwen (2015) #14 (series #20505)
    - Spider-Man/Deadpool (2016) #11 (series #19679)
    - Star Wars: The Force Awakens Adaptation (2016) #6 (series #21493)
    - The Avengers (2016) #1.1 (series #22966)
    - The Clone Conspiracy (2016) #2 (series #22654)
    - Thunderbolts (2016) #7 (series #20884)
    - Uncanny Avengers (2015) #16 (series #20621)
    - Uncanny X-Men (2016) #15 (series #20612)
