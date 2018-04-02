# pairmaker
Flask app to make ~random~ pairs of users &amp; optimize for reduced duplicates

## Todo: write the dang README

In the meantime, the app serves a single endpoint: `/call`

It expects a call in Slack webhook format. Namely, it's looking to the body of `request.json.text` to determine how to handle the call.
Current supported calls are:

- `<botname> add <username> <office>` - adds a user to a given office
- `<botname> remove <username>` - remove a user
- `<botname> list` - lists all users and their office
- `<botname> pairup` - returns a pair of users who are in *different offices*.

The response is in the format `{'text': '<response>'}`. In this way, Slack will present the body of the response directly as a message from the bot.

The pairing algorithm is pretty simple but effective for mixing things up:
- First it picks the user who has not been picked in the longest time.
- Then it pairs that user with the user who has not been paired with that person in the longest time.
