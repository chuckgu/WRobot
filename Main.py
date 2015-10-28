#-*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from Templates import Template
from datetime import datetime

start_date='20151006'
end_date='20151006'

datetimeobject = datetime.strptime(start_date,'%Y%m%d')

model=Template(start_date,1)
model.build()


article=model.write()

print "[시황기사] " + " (" + datetimeobject.strftime('%Y-%m-%d') + ")"
final=''
for ar in article:
    final=final+' '+ar
    
print final
print '\n'






