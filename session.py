import database
import config
from bson.objectid import ObjectId

sync = config.SyncInLine()


def do_session():
    # iç içe importu engellemek içn bu dizinde açıyorum
    from backdoor import get_ip_data
    #  backdoor servisinin getirdiği veriler i db e kayıt edip gelen id i d dizin züerine yazıyor
    session_id = database.create_session(get_ip_data())
    #  session id set ediyoruz
    sync.set('SESSION_ID', str(session_id))
    config.SESSION_ID = session_id


def get_session():
    return ObjectId(sync.get('SESSION_ID'))


