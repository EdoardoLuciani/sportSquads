# sportSquads

sportSquads is a space offering users the opportunity to find
other sport enthusiasts and get together to play their favourite
sports.
Every user can choose their favourite sport and create their own
team or join someone else’s within just a few clicks! The users
can pick the team they best fit in, through their description,
location, and the availability of spots in their preferred role.
Is the sport you are interested not there? You can just add your
own sport category and team for others to join!
No commitment is necessary since every user can drop out and
give a shot to a different team or even sport!
Users can also join an unlimited number of teams through their
account and try new sports along the way

## Getting started

### Dependencies

In order to run sportSquads, the following dependencies are required (also found in requirements.txt):

`pillow==8.4.0
django==4.0.2`

### Initialize the database (SQLite)

Once you cloned the repo, navigate to the newly created directory, and input these commands to create and setup the underlying database:

`python manage.py migrate`

`python manage.py createsuperuser`

Then run the population script to populate it with sample data (it takes a while so give it a little bit of time)

`python populate_sportSquads.py`

### Usage

At this point everything should be good to go! Start the server by typing:

`python manage.py runserver`

Note: In order to access all website's features (create/delete team and create/delete sport) an account is needed. The admin account created earlier
does not count.

## Tests

Tests are available and can be run with:
`python manage.py test sportSquads`

## License

Distributed under the MIT License. See LICENSE.txt for more information.

