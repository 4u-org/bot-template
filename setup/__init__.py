from setup.startup import startup
from setup.shutdown import shutdown

import config as cnf

if cnf.LOCAL:
    print("LOCAL START")
    from setup.local_start import start_bot
else:
    print("SERVER START")
    from setup.server_start import start_bot