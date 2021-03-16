import logging
from typing import Optional, Union

from ..proto.email_pb2 import EmailMessage
from ..proto.slack_pb2 import SlackMessage
from ..ns_client.dataclasses import ERPNSConfiguration
from ..ns_client.pika import PikaPublisher
from ..ns_client.settings import erp_ns_client_settings

log = logging.getLogger(__name__)


class NSClient:
    def __init__(self, configuration: Optional[ERPNSConfiguration] = None):
        self.conf = configuration or ERPNSConfiguration(
            URI=erp_ns_client_settings.RMQ_URI,
            EXCHANGE=erp_ns_client_settings.RMQ_EXCHANGE,
            SLACK_QUEUE=erp_ns_client_settings.RMQ_PUBS_SLACK_QUEUE,
            SLACK_TOPIC=erp_ns_client_settings.RMQ_PUBS_SLACK_TOPIC,
            EMAIL_QUEUE=erp_ns_client_settings.RMQ_PUBS_EMAIL_QUEUE,
            EMAIL_TOPIC=erp_ns_client_settings.RMQ_PUBS_EMAIL_TOPIC,
            SLACK_ROUTING_KEY_PREFIXES_INTERACTIVE=(
                erp_ns_client_settings.RMQ_SUBS_SLACK_ROUTING_KEY_PREFIXES_INTERACTIVE
            ),
            SLACK_ROUTING_KEY_PREFIXES_EVENTS=(
                erp_ns_client_settings.RMQ_SUBS_SLACK_ROUTING_KEY_PREFIXES_EVENTS
            ),
            SLACK_ACCESS_TOKEN=erp_ns_client_settings.RMQ_SLACK_ACCESS_TOKEN,
        )
        self.exchange = self.conf.EXCHANGE
        self.headers = {}
        self.topic = None
        self.queue = None

        self.publisher = PikaPublisher(uri=self.conf.URI)

    @staticmethod
    def to_proto(msg: Union[SlackMessage, EmailMessage]):
        return msg.SerializeToString()

    def send(
        self,
        message: Union[SlackMessage, EmailMessage],
        routing_key: Optional[str] = None,
        close_connection: Optional[bool] = True,
    ):
        topic = routing_key or self.topic
        self.publisher.publish(
            message=self.to_proto(msg=message),
            exchange=self.exchange,
            routing_key=topic,
            headers=self.headers,
            close_connection=close_connection,
        )


class NSSlackClient(NSClient):
    def __init__(
        self, configuration: Optional[ERPNSConfiguration] = None, access_token: str = None
    ):
        super(NSSlackClient, self).__init__(configuration=configuration)
        self.queue = self.conf.SLACK_QUEUE
        self.topic = self.conf.SLACK_TOPIC
        self.headers = {"X-Slack-Access-Token": access_token or self.conf.SLACK_ACCESS_TOKEN}
        self.SUBSCRIBTION_TYPES = {
            "events": self.conf.SLACK_ROUTING_KEY_PREFIXES_EVENTS,
            "interactive": self.conf.SLACK_ROUTING_KEY_PREFIXES_INTERACTIVE
        }


class NSEmailClient(NSClient):
    def __init__(self, configuration: Optional[ERPNSConfiguration] = None):
        super(NSEmailClient, self).__init__(configuration=configuration)
        self.queue = self.conf.EMAIL_QUEUE
        self.topic = self.conf.EMAIL_TOPIC


slack_postman = NSSlackClient()
email_postman = NSEmailClient()
