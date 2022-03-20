from maubot import Plugin, MessageEvent
from maubot.handlers import command, event
from mautrix.types import EventType


class AlternatingCaps(Plugin):
    last_message = None

    @event.on(EventType.ROOM_MESSAGE)
    async def message_handler(self, evt: MessageEvent) -> None:
        self.last_message = evt.content.body

    @command.new()
    async def altcaps(self, evt: MessageEvent) -> None:
        if self.last_message:
            await evt.respond("".join([c.upper() if i % 2 else c.lower() for i, c in enumerate(self.last_message)]))
