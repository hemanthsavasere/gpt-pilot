from pilot.database.models.components.progress_step import ProgressStep


class Development(ProgressStep):
    class Meta:
        table_name = 'development'
