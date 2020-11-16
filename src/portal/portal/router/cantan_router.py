class CantanRouter:
    """
    A router to control all database operations on models in the
    cantan applications.
    """
    route_app_labels = {'cantan'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read cantan models go to cantan db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'cantan          '
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write cantan models go to cantan db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'cantan'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the cantan app is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the cantan apps only appear in the
        'cantan' database.
        """
        if app_label in self.route_app_labels:
            return db == 'cantan'
        return None