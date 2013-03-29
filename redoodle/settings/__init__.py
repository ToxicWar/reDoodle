#platform.node()
#socket.gethostname()
#os.environ['COMPUTERNAME']


#the simple way:
import platform
if platform.node() == '1225c':
	from v_3bl3 import *
else:
	from v_4ui import *


#exclusive way for 4ui who hates if's
#import os
#import platform
#FILES = {
#	'1225c':  "v_3bl3",
#	'4ui-pc': "v_4ui"
#}
#pc_name = platform.node()
#execfile(os.path.join("redoodle", "settings", FILES[pc_name] + ".py"))

