import database
import config


def do_session():
    from backdoor import get_ip_data
    config.SESSION_ID = database.create_session(get_ip_data())


def get_session():
    from config import SESSION_ID
    return SESSION_ID
