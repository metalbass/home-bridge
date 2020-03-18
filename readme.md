# Home Bridge

Add devices to Google's [Home Graph] by creating
configuring them through [Django's admin site](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/).

## Status
- Devices added to the database are visible from [Home Graph] and Google Assistant.
- Actions from Google Assistant call `execute_command` methods on `Device` subclasses.
- No integration between `execute_command` and real devices has been coded or properly designed yet.

## Usual commands during development

### Django commands
All listed commands are invoked through `py manage.py`.

They can also be called over Heroku through `heroku run python manage.py`. 

| Command                    | Description                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------- |
| `makemigrations`           | Creates new migrations based on the changes detected to your models.                   |
| `migrate`                  | Synchronizes the database state with the current set of models and migrations.         |
| `createsuperuser`          | Creates a django user to use through the admin site.                                   |
| `test`                     | Runs unit tests.                                                                       |


### Heroku commands

All listed commands are invoked through `heroku`.

| Command                    | Description                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------- |
| `run`                      | Runs the given command in the live Heroku instance.                                |
| `pg:reset`                 | Resets the postgres db.                                                                |


[Home Graph]: https://developers.google.com/assistant/smarthome/concepts/homegraph
