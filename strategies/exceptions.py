


class StopBotError(Exception):
    """exception to interrupt bot
    """
    message = "Full bot interupt"


class SignalRestartError(Exception):
    """exception signal restart
    """
    message = "signaling restart"
    