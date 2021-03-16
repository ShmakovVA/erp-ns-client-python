from pydantic import BaseSettings


class ERPNSClientSettings(BaseSettings):
    RMQ_URI: str
    RMQ_EXCHANGE: str
    RMQ_PUBS_SLACK_QUEUE: str
    RMQ_PUBS_SLACK_TOPIC: str
    RMQ_SUBS_SLACK_ROUTING_KEY_PREFIXES_INTERACTIVE: str
    RMQ_SUBS_SLACK_ROUTING_KEY_PREFIXES_EVENTS: str
    RMQ_PUBS_EMAIL_QUEUE: str
    RMQ_PUBS_EMAIL_TOPIC: str
    RMQ_SLACK_ACCESS_TOKEN: str


erp_ns_client_settings = ERPNSClientSettings()
