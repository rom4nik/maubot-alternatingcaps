from maubot import Plugin, MessageEvent
from maubot.handlers import command, event
from mautrix.types import EventType


class AlternatingCaps(Plugin):
    last_messages = {}

    @event.on(EventType.ROOM_MESSAGE)
    async def message_handler(self, evt: MessageEvent) -> None:
        self.last_messages[evt.room_id] = evt.content.body

    @command.new()
    async def altcaps(self, evt: MessageEvent) -> None:
        if evt.room_id in self.last_messages:
            await evt.respond("".join([c.upper() if i % 2 else c.lower() for i, c in enumerate(self.last_messages[evt.room_id])]))
