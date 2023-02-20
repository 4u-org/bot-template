from setup.startup import main_startup
from setup.shutdown import main_shutdown

import config as cnf

if cnf.LOCAL:
    print("LOCAL START")
    from setup.local_register import register_main_bot
else:
    print("SERVER START")
    from setup.server_register import register_main_bot