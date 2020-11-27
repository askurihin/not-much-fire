from email.utils import parseaddr

from notmuch import Message

class Notifi2Notifier:
    def __init__(self, app_name: str):
        """Initialize the connection to the notification daemon.

        Required to being able sending notifications later on. The
        registered application name can be used to filter notification
        at the daemon itself for special handling.
        """

        notify2.init(app_name)

    def notify_message(self, message: Message) -> None:
        """Formats the message into a notification and send it to the daemon.

        Uses the name of the sender as notification title. In case such
        is not defined, the mail address is used instead. As body of the
        notification the message subject is used. The formatted message
        is send to the systems notification daemon.
        """
        name, address = parseaddr(message.get_header("from"))
        sender = name or address
        subject = message.get_header("subject")
        notification = notify2.Notification(sender, subject)
        notification.show()

class PyncNotifier:
    def __init__(self, app_name: str):
        pass


    def notify_message(self, message: Message) -> None:
        """Formats the message into a notification and send it to the daemon.

        Uses the name of the sender as notification title. In case such
        is not defined, the mail address is used instead. As body of the
        notification the message subject is used. The formatted message
        is send to the systems notification daemon.
        """
        import pync
        name, address = parseaddr(message.get_header("from"))
        sender = name or address
        subject = message.get_header("subject")
        pync.notify(title=sender, message=f"'{subject}'")


def Notifier(app_name: str):  # noqa
    try:
        import notify2
        return Notifi2Notifier(app_name)
    except ImportError:
        import pync
        return PyncNotifier(app_name)

