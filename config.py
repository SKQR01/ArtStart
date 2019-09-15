### Класс конфигурации ###
class Conf(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\Python\ArtStat\data\db.db'

    UPLOAD_FOLDER = 'D:\Python\ArtStat\static\img'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webp'])

    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    
   