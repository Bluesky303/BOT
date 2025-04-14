from bot_core import plugin_setup, on_event

@plugin_setup
def setup():
    @on_event("message")
    def on_message(event):
        print(event)