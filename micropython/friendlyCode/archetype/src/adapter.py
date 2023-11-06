from .event import Event

class Target:
    """
    The Target defines the domain-specific interface used by the client code.
    """

    def request(self) -> str:
        raise NotImplementedError


class Adaptee:
    """
    The Adaptee contains some useful behavior, but its interface is incompatible
    with the existing client code. The Adaptee needs some adaptation before the
    client code can use it.
    """

    def specific_request(self):
        raise NotImplementedError


class Adapter(Target, Adaptee):

    def set_specific_request(self, specific_request: callable):
        self.specific_request = specific_request

    def request(self) -> Event:
        return self.specific_request()