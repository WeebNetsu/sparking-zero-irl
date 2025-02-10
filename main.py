from time import sleep

from modules.app import App
from modules.config_loader import ConfigLoader

print("Program will start in 5 seconds")
sleep(5)

app_config = ConfigLoader()
app = App(app_config)
app.run()
