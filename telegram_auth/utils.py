import json
import hashlib
import hmac
from dataclasses import dataclass, field
from json import JSONDecodeError
from operator import itemgetter
from urllib.parse import parse_qsl

@dataclass
class User:
    id: int = field(default=None)
    first_name: str = field(default=None)
    is_premium: bool = field(default=None)
    allows_write_to_pm: bool = field(default=None)
    language_code: str = field(default=None)
    last_name: str = field(default=None)
    username: str = field(default=None)

    def __init__(self, **kwargs):
        if kwargs:
            for field in self.__dataclass_fields__:
                if field in kwargs:
                    setattr(self, field, kwargs[field])
                else:
                    setattr(self, field, self.__dataclass_fields__[field].default)

def check_webapp_signature(token: str, init_data: str) -> (bool, User):
    """
    Check incoming WebApp init data signature

    Source: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    :param token:
    :param init_data:
    :return:
    """
    try:
        parsed_data = dict(parse_qsl(init_data))
    except ValueError:
        # Init data is not a valid query string
        return False
    if "hash" not in parsed_data:
        # Hash is not present in init data
        return False

    hash_ = parsed_data.pop('hash')
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()

    user_data = User()
    if 'user' in parsed_data.keys():
        try:
            user_data = User(**json.loads(parsed_data['user']))
        except JSONDecodeError:
            pass

    return calculated_hash == hash_, user_data
