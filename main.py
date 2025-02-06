from modules.app import App
from modules.config_loader import ConfigLoader

app_config = ConfigLoader()
app = App(app_config)
app.run()
