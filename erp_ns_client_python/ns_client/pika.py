import logging
from typing import Dict, Optional

from pika import BasicProperties, BlockingConnection, ConnectionParameters, PlainCredentials
from pika.exceptions import UnroutableError
from pika.spec import PERSISTENT_DELIVERY_MODE
from urllib3.util import parse_url

log = logging.getLogger(__name__)


class PikaPublisher:
    PROPS = BasicProperties(delivery_mode=PERSISTENT_DELIVERY_MODE)

    def __init__(self, uri: str, confirm_delivery: Optional[bool] = True):
        self.uri = uri
        self.confirm_delivery = confirm_delivery
        self.connection, self.channel = self._re_init()

    def _re_init(self, uri: Optional[str] = None):
        self.connection = self.__new_connection(uri=uri)
        self.channel = self.__new_channel()
        log.info("A new connection initiated")
        return self.connection, self.channel

    def __new_connection(self, uri: Optional[str] = None):
        uri = uri or self.uri
        # TODO: verify uri somehow
        parsed = parse_url(uri)
        user_, pass_ = parsed.auth.split(":")
        params = (
            ConnectionParameters(
                host=parsed.host,
                port=parsed.port,
                credentials=PlainCredentials(username=user_, password=pass_),
                connection_attempts=5,
                retry_delay=1,
            ),
        )
        # TODO: check auth
        return BlockingConnection(parameters=params)

    def __new_channel(self, confirm_delivery: Optional[bool] = True):
        channel = self.connection.channel()
        if confirm_delivery:
            channel.confirm_delivery()
        return channel

    def publish(
        self,
        message: bytes,
        exchange: str,
        routing_key: str,
        close_connection: bool = True,
        headers: Dict = None,
    ):
        if self.connection is None or self.channel is None:
            self._re_init()
        self.PROPS.headers = headers

        success = False
        try:
            self.channel.basic_publish(
                exchange=exchange, routing_key=routing_key, body=message, properties=self.PROPS
            )
        except UnroutableError:
            log.error("Message could not be confirmed")
        else:
            log.info("Message publish was confirmed")
            success = True

        if close_connection:
            self.connection.close()
            self.connection = self.channel = None
            log.info("Connection was closed by user request")

        return success
