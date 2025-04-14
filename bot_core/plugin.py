from importlib import import_module
from typing import Dict, Any, Callable
from pathlib import Path

from bot_core.listener import EventListener

'''
插件示例：
@plugin_setup(listener)
class Setup:
    @on_event("message", lambda event: hasattr(event, "content") and event.content == "hello"):
        def hello(self, event):
            print("Hello, world!")

    @on_event("message", lambda event: hasattr(event, "content") and event.content == "bye"):
        def bye(self, event):
            print("Bye, world!")
            
当插件为包时需要有__init__.py文件，文件中导入所有插件类
'''

# 管理器类
class PluginManager:
    def __init__(self, listener: EventListener):
        self.listener = listener
        self.plugins: Dict[str, Any] = {}
        self.plugins_path = Path("plugins")
        
    def load_plugins(self, plugin_name: str):
        try:
            print(f"Loading plugin {plugin_name}")
            # 导入插件
            module = import_module(f"plugins.{plugin_name}")
            # 检查是否有插件类
            has_cls = False
            # 遍历所有插件类
            for attr in dir(module):
                cls = getattr(module, attr)
                if hasattr(cls, "_is_plugin") and cls._is_plugin:
                    # 注册所有监听器
                    self._register_handlers(cls)
                    self.plugins[plugin_name] = cls
                    has_cls = True
            if has_cls:
                print(f"Loaded plugin {plugin_name}")
            else:
                print(f"Plugin {plugin_name} has no required class")
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {e}")
            
    def _register_handlers(self, cls):
        # 遍历所有监听器
        for attr in dir(cls):
            method = getattr(cls, attr)
            if hasattr(method, "_config"):
                print(f"Registered handler {method._config['name']}")
                self.listener.register_handler(method._config["name"], method._config["condition"], method)
                
    def unload_plugins(self, plugin_name: str):
        # 需要卸载监听器，懒得写了
        self.plugins.pop(plugin_name)
        print(f"Unloaded plugin {plugin_name}")
        
    def load_all_plugins(self):
        for plugin in self.plugins_path.iterdir():
            if plugin.name.startswith(("_", ".")): # 特殊文件忽略
                continue
            if plugin.is_dir() and (plugin / "__init__.py").exists(): # 包
                self.load_plugins(plugin.name)
            if plugin.suffix == ".py": # 单文件
                self.load_plugins(plugin.stem)

# 装饰器
def plugin_setup():
    def decorator(cls):
        # 添加装饰标记
        cls._is_plugin = True
        return cls
    return decorator

def on_event(name: str, condition: Callable):
    def decorator(method):
        # 添加装饰标记
        method._config = {"name": name, "condition": condition}
        return method
    return decorator