from django.apps import AppConfig

class TeamsportsConfig(AppConfig):
    name = 'teamsports'
    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Photo'))
        registry.register(self.get_model('Schedule'))
        registry.register(self.get_model('GameNotes'))
        from watson import search as watson
        watson.register(self.get_model('Schedule'))
        watson.register(self.get_model('Teams'))
        watson.register(self.get_model('School'))
