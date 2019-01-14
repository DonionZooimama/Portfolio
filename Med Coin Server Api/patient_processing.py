import random
import qrtools
import base64

database_directory = "database.csv"


def UpdatePatientData(myid, name, age, bloodtype,medications, allergies):
    with open(database_directory, 'r') as file:
        data = file.readlines()
        index = 0
        found = False
        for line in data:
            if int(line.split(',')[0]) == int(myid):
                found = True
                new_line = "%s,%s,%s,%s,%s,%s,\n" % (myid, name, age, bloodtype, medications, allergies)
                data[index] = new_line
                break
            index += 1

    if found:
        with open(database_directory, 'w') as file:
            file.writelines(data)
            return 1
    else:
        return myid + " does not exist"


def NewPatientData(first, last, bloodtype, allergies):
    with open(database_directory, 'r') as file:

        r = random.randint(100000000000, 999999999999)
        run = True
        while run:
            run = False
            for line in file:
                if int(line.split(',')[0]) == r:
                    r = random.randint(100000000000, 999999999999)
                    run = True
                    break

    with open(database_directory, 'a') as file:
        line = "%s,%s,%s,%s,%s,\n" % (r, first, last, bloodtype, allergies)
        file.write(line)
        return str(r) + " successfully created"

def GetPatientData():
    qr = qrtools.QR()
    qr.decode('temp.jpg')

    if qr.data != 'NULL':
        my_id = int(qr.data)
        with open(database_directory, 'r') as file:
            data = file.readlines()
            for line in data:
                if int(line.split(',')[0]) == my_id:
                    return line
        return 0
    else:
        return -1