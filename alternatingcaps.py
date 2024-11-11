from maubot import Plugin
from maubot.handlers import command, event
from mautrix.types import EventType, MessageEvent, RedactionEvent


class AlternatingCaps(Plugin):
    last_messages = {}

    def is_alias(self, command: str) -> bool:
        return command == 'altcaps' or command in ["spongebob", "alternatingcaps"]

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

    @command.new(aliases=is_alias)
    async def altcaps(self, evt: MessageEvent) -> None:
        if evt.content.get_reply_to():
            target = await self.client.get_event(evt.room_id, evt.content.get_reply_to())
            body = target.content.body
        elif evt.room_id in self.last_messages:
            body = self.last_messages[evt.room_id]["body"]

        await evt.respond("".join([c.upper() if i % 2 else c.lower() for i, c in enumerate(body)]))
