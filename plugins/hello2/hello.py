from bot_core.plugin import plugin_setup, on_event

@plugin_setup()
class Setup:
    @on_event("message", lambda event: hasattr(event, "message"))
    async def hello(event):
        print("Hello, world!")
    
    @on_event("message", lambda event: hasattr(event, "message"))
    async def bye(event):
        print("Bye, world!")