from dataclasses import dataclass


@dataclass
class ERPNSConfiguration:
    URI: str
    EXCHANGE: str

    SLACK_QUEUE: str
    SLACK_TOPIC: str
    SLACK_ROUTING_KEY_PREFIXES_INTERACTIVE: str
    SLACK_ROUTING_KEY_PREFIXES_EVENTS: str

    EMAIL_QUEUE: str
    EMAIL_TOPIC: str

    SLACK_ACCESS_TOKEN: str
