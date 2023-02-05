from keys import PUBLIC_KEY, PRIVATE_KEY
import hashlib
import time

# Función para generar el payload requerido por la API
def generate_payload() -> dict[str, str]:
    # Crea el payload
    ts = f'{time.time_ns()}'

    apikey = ts + PRIVATE_KEY + PUBLIC_KEY
    apikey = apikey.encode('utf-8')
    hash =  hashlib.md5(apikey).hexdigest()

    payload = {
        'ts': ts,
        'apikey': PUBLIC_KEY,
        'hash': hash,
    }

    return payload