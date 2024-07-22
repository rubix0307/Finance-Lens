import hashlib
import hmac
import json
import time


def verify_telegram_webapp(data_dict, bot_token):
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    check_hash = data_dict.pop('hash')
    data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(data_dict.items())])
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac_hash == check_hash and time.time() < int(data_dict['auth_date']) + 86400  # 24 hours


# Пример параметров
params = {
    'tgWebAppData': [
        'user={"id":5970474467,"first_name":"Артем","last_name":"","username":"xx_rubix_xx_kyiv","language_code":"ru","allows_write_to_pm":true}'],
    'chat_instance': ['-9154240853419557181'],
    'chat_type': ['private'],
    'start_param': ['kentId887832606'],
    'auth_date': ['1721681182'],
    'hash': ['28f6e4a2f6cf82d3e0c0577efce7b8f5881cbe4c2fba0cda4307d8e4c81a7059'],
}

# Извлечение и декодирование tgWebAppData
tgWebAppData = json.loads(params['tgWebAppData'][0].split('user=')[1])

# Подготовка данных для верификации
data = {
    'id': tgWebAppData['id'],
    'first_name': tgWebAppData['first_name'],
    'last_name': tgWebAppData.get('last_name', ''),
    'username': tgWebAppData['username'],
    'language_code': tgWebAppData['language_code'],
    'allows_write_to_pm': tgWebAppData['allows_write_to_pm'],
    'auth_date': params['auth_date'][0],
    'hash': params['hash'][0]
}

# Ваш токен бота
bot_token = 'YOUR_BOT_TOKEN'

# Верификация
if verify_telegram_webapp(data, bot_token):
    print("User is verified")
else:
    print("Verification failed")
