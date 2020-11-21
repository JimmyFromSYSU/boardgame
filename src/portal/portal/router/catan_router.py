class CatanRouter:
    """
    A router to control all database operations on models in the
    catan applications.
    """
    route_app_labels = {'catan'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read catan models go to catan db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'catan'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write catan models go to catan db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'catan'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the catan app is
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
        Make sure the catan apps only appear in the
        'catan' database.
        """
        if app_label in self.route_app_labels:
            return db == 'catan'
        return None