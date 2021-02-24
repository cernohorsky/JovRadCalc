file1=open('jupiter_horizons_results.txt','r')
file2=open('io_horizons_results.txt','r')
LinesJup=file1.readlines()
LinesIo=file2.readlines()

i=0
j=0

def compute(inputstr):
    s=''

    if inputstr=='':
        return s

    elev=float(inputstr[31:40])
    if float(elev)>-90:
        cml=float(inputstr[41:52])
        io_phase=float(inputstr[64:75])

        if cml < 255 and cml > 200 and io_phase < 250 and io_phase > 220:
            s='Io-A'

        if cml < 180 and cml > 105 and io_phase < 100 and io_phase > 80:
            s='Io-B'

        if cml < 350 and cml > 300 and io_phase < 250 and io_phase > 230:
            s='Io-C'
    return s

while LinesIo[i]!='$$SOE\n':
    i=i+1

while LinesJup[j]!='$$SOE\n':
    j=j+1

i=i+1
j=j+1

while LinesJup[j]!='$$EOE\n':
    input_values = LinesJup[j].rstrip("\n")+' '+LinesIo[i][40:50]
    #print(input_values)
    result = compute(input_values)
    if result!='':
        begin=LinesJup[j][1:18]
        x=result
        while x!='':
            i=i+1
            j=j+1
            x=compute(LinesJup[j].rstrip("\n")+' '+LinesIo[i][40:50])
        end=LinesJup[j][13:18]
        outstring=begin+' '+end+' '+str(result)
        print(outstring)

    i=i+1
    j=j+1
