from peewee import TextField
from pilot.database.models.components.progress_step import ProgressStep


class ProjectDescription(ProgressStep):
    prompt = TextField()
    summary = TextField()

    class Meta:
        table_name = 'project_description'
