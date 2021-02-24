from pichi.models.api import Message


def get_heartbeat() -> Message:
    return Message(
        message="I feel FANTASTIC and I'm still alive.",
    )
