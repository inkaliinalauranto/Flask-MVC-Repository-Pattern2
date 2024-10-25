# Tarkoituksena on, että valmiissa koodissa ylikirjoitetaan
# UsersRepositoryn (yliluokan) get_all-metodi tämän luokan toteutuksella
class UserRepositoryJSONPlaceholder:
    def __init__(self, con):
        self.con = con

    def get_all(self):
        pass