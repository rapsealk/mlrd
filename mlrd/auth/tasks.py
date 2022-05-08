import json

import pika

from mlrd.auth.schema import UserRead


def publish_user_signup_event(
    routing_key: str,
    user: UserRead
):
    """사용자의 회원가입 이벤트를 생성 및 메시지 큐에 발송합니다.

    본 이벤트를 수신하는 마이크로서비스는 아래와 같습니다.
    - Mail (https://github.com/rapsealk/mlrd-microservice-mail)

    본 이벤트의 payload는 아래와 같습니다.
    - 사용자의 이메일 주소 (email)
    - 사용자 인증 링크 (url)

    Args:
        :param routing_key: ...
        :param user: ...
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    payload = json.dumps({
        "email": user.email,
        "url": "http://localhost:8000/user/verify"
    })

    channel.queue_declare(queue="signup")
    channel.basic_publish(exchange="", routing_key=routing_key, body=payload)
