marvelous
=========

Marvel API python wrapper.

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
        'dateDescriptor': "thisWeek"}),
        key=lambda comic: comic.title)

    # Grab the sale date of any of the comics for the folder name
    directory = pulls[0].dates.on_sale.strftime('%m-%d')

    # If there's no folder by that name, create one
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a pulls.txt file in that folder
    with open(directory + '/pulls.txt', 'w') as pull_checklist:
        # Check each comic that came out this week
        for comic in pulls:
            # If this series isn't in my ignore list
            if comic.series.id not in IGNORE:
                # Write a line to the file with the name of the issue, and the
                # id of the series incase I want to add it to my ignore list
                pull_checklist.write('{} (series #{})\n'.format(
                    comic.title.encode('utf-8'), comic.series.id))
