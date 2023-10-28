from maubot import Plugin
from maubot.handlers import command, event
from mautrix.types import EventType, MessageEvent, RedactionEvent


class AlternatingCaps(Plugin):
    last_messages = {}

    @event.on(EventType.ROOM_MESSAGE)
    async def message_handler(self, evt: MessageEvent) -> None:
        if evt.sender != self.client.mxid:
            self.last_messages[evt.room_id] = {
                "id": evt.event_id,
                "body": evt.content.body
            }

    @event.on(EventType.ROOM_REDACTION)
    async def redaction_handler(self, evt: RedactionEvent) -> None:
        if evt.room_id in self.last_messages and evt.redacts == self.last_messages[evt.room_id]["id"]:
                self.last_messages.pop(evt.room_id)

    @command.new()
    async def altcaps(self, evt: MessageEvent) -> None:
        if evt.room_id in self.last_messages:
            await evt.respond("".join([c.upper() if i % 2 else c.lower() for i, c in enumerate(self.last_messages[evt.room_id]["body"])]))
