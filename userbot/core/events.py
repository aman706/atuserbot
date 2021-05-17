import inspect
import asyncio
import re
from telethon import events, functions, types, utils
from telethon.events.common import EventCommon
from telethon.tl.custom.sendergetter import SenderGetter

from .inlinebuilder import InlineBuilder
from .managers import edit_or_reply


@events.common.name_inner_event
class NewMessage(events.NewMessage):
    def __init__(self, require_admin: bool = None, inline: bool = False, **kwargs):
        super().__init__(**kwargs)

        self.require_admin = require_admin
        self.inline = inline

    def filter(self, event):
        _event = super().filter(event)
        if not _event:
            return

        if self.inline is not None and bool(self.inline) != bool(
            event.message.via_bot_id
        ):
            return

        if self.require_admin and not isinstance(event._chat_peer, types.PeerUser):
            is_creator = False
            is_admin = False
            creator = hasattr(event.chat, "creator")
            admin_rights = hasattr(event.chat, "admin_rights")
            if not creator and not admin_rights:
                event.chat = event._client.loop.create_task(event.get_chat())

            if self.incoming:
                try:
                    p = event._client.loop.create_task(
                        event._client(
                            functions.channels.GetParticipantRequest(
                                event.chat_id, event.sender_id
                            )
                        )
                    )
                    participant = p.participant
                except Exception:
                    participant = None
                if isinstance(participant, types.ChannelParticipantCreator):
                    is_creator = True
                if isinstance(participant, types.ChannelParticipantAdmin):
                    is_admin = True
            else:
                is_creator = event.chat.creator
                is_admin = event.chat.admin_rights

            if not is_creator and not is_admin:
                text = "`I need admin rights to be able to use this command!`"

                event._client.loop.create_task(edit_or_reply(event, text))
                return
        return event


@events.common.name_inner_event
class InlineQuery(events.common.EventBuilder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def build(cls, update, others=None, self_id=None):
        if isinstance(update, types.UpdateBotInlineQuery):
            return cls.Event(update)

    class Event(EventCommon, SenderGetter):
        def __init__(self, query):
            super().__init__(chat_peer=types.PeerUser(query.user_id))
            SenderGetter.__init__(self, query.user_id)
            self.query = query
            self.pattern_match = None
            self._answered = False

        def _set_client(self, client):
            super()._set_client(client)
            self._sender, self._input_sender = utils._get_entity_pair(
                self.sender_id, self._entities, client._entity_cache
            )

        @property
        def text(self):
            return self.query.query

        @property
        def catbuilder(self):
            return InlineBuilder(self._client)

        async def answer(
            self,
            results=None,
            cache_time=0,
            *,
            gallery=False,
            next_offset=None,
            private=False,
            switch_pm=None,
            switch_pm_param=""
        ):
            if self._answered:
                return
            if results:
                futures = [self._as_future(x) for x in results]

                await asyncio.wait(futures)
                results = [x.result() for x in futures]
            else:
                results = []
            if switch_pm:
                switch_pm = types.InlineBotSwitchPM(switch_pm, switch_pm_param)
            return await self._client(
                functions.messages.SetInlineBotResultsRequest(
                    query_id=self.query.query_id,
                    results=results,
                    cache_time=cache_time,
                    gallery=gallery,
                    next_offset=next_offset,
                    private=private,
                    switch_pm=switch_pm,
                )
            )

        @staticmethod
        def _as_future(obj):
            if inspect.isawaitable(obj):
                return asyncio.ensure_future(obj)

            f = asyncio.get_event_loop().create_future()
            f.set_result(obj)
            return f


@events.common.name_inner_event
class MessageEdited(NewMessage):
    @classmethod
    def build(cls, update, others=None, self_id=None):
        if isinstance(update, types.UpdateEditMessage):
            return cls.Event(update.message)
        elif isinstance(update, types.UpdateEditChannelMessage):
            if (
                update.message.edit_date
                and update.message.is_channel
                and not update.message.is_group
            ):
                return
            return cls.Event(update.message)

    class Event(NewMessage.Event):
        pass
