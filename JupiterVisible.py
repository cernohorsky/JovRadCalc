
import datetime

JupiterOppositionDay=231
JupiterOppKulTime=datetime.datetime(2021,8,19,1,36)
timewindow=4*60*60

file=open('jovrad.csv', 'r')
Lines = file.readlines()

#count=0
for count in range(5,len(Lines)-1):
    #count+=1
    line = Lines[count].split()

    if float(line[6])<4.3: #Jupiter must be closer as 4.3 AU
        datestr=line[1]+' '+line[2]
        date=datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        
        # Kulmination times
        kulmination=JupiterOppKulTime
        kulminationNext=JupiterOppKulTime
        
        if int(line[0])>=JupiterOppositionDay:
            #kulmination=JupiterOppKulTime + datetime.timedelta(days=(int(line[0])-JupiterOppositionDay+1),minutes=-((int(line[0])-JupiterOppositionDay)*4.28571))
            kulmination=JupiterOppKulTime + datetime.timedelta(days=(int(line[0]))-JupiterOppositionDay)
            kulmination=kulmination - datetime.timedelta(minutes=(int(line[0])-JupiterOppositionDay)*4.28571)
            kulminationNext=kulmination + datetime.timedelta(days=1,minutes=-4.28571)

        if int(line[0])<JupiterOppositionDay:
            kulmination=JupiterOppKulTime - datetime.timedelta(days=(JupiterOppositionDay-int(line[0])))
            kulmination=kulmination + datetime.timedelta(minutes=((JupiterOppositionDay-int(line[0]))*4.28571))

        td1=(date-kulmination).total_seconds()
        td2=(kulmination-date).total_seconds()
        td3=(kulminationNext-date).total_seconds()
        if abs(td1)<abs(td3):
            td=abs(td1)
        else:
            td=abs(td3)

        if td<timewindow:
            print(line)
            '''
            print(kulmination)
            print(td1/3600)
            print(td2/3600)
            print(td3/3600)
            '''
