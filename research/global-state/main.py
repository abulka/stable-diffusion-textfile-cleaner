# https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules

import config
import mod
print(config.x)

config.x = 200
mod.report_x()
