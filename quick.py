from datetime import datetime

with open('quick.txt', 'w') as fout:
    fout.write(str(datetime.now()))
    fout.write('this is here')