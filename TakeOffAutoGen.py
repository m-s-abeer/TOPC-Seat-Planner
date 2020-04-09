import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import random

class arrange:
    def __init__ (self, filepath="topcfall19.csv"):
        self.filepath = filepath
        self.dataframe = pd.read_csv(filepath)
        self.cleandata()
        self.semester1 = self.dataframe[self.dataframe.semester == '1st']
        self.semester2 = self.dataframe[self.dataframe.semester == '2nd']
        self.planseat(nocomputer = 35, roomcount = 8)

    def cleandata(self):
        print("Cleaning Data... ")
        df = self.getdataframe()
        df = df[df.payment == 'OK']
        df = df.sample(frac = 1)
        self.setdataframe(df)

    def getsectionwiseregistration(self):
        df1 = self.get1stsemester()
        df2 = self.get2ndsemester()
        f, (ax1, ax2) = plt.subplots(ncols=2)
        f.suptitle('Section vs Registration ratio.', fontsize='16')
        df1.groupby('section').section.count().plot(ax=ax1, color='#1976D2', kind='bar')
        ax1.set_title('1st Semester (total: ' + str(df1.id.count()) + ')')
        df2.groupby('section').section.count().plot(ax=ax2, color='#1976D2', kind='bar')        
        ax2.set_title('2nd Semester (total: ' + str(df2.id.count()) + ')')
        plt.show()

    def planseat(self, nocomputer, roomcount, rooms=[601, 602, 701, 702, 801, 802, 901, 902], columncount=8, rowcount=5):
        print("Processing Data.. ")
        #distribute the students token wise without shuffling
        roomwisetoken = self.distributetoken(nocomputer, roomcount)
                        
        #make the seatrange csv
        self.saveseatplanrange(roomwisetoken, rooms)

        #make tshirt room wise count
        self.tshirtcountsave(roomwisetoken, rooms)

        #shuffle the seatplan
        self.shuffleseatarrangement(35, roomwisetoken)

        #save roomwise seatplan
        self.saveseatplanindividual(rooms, roomwisetoken)

        # return roomwisetoken

    def saveseatplanindividual(self, rooms, roomwisetoken):
        print("Saving seatplan for rooms.")
        with open('seatplan.csv', 'w+', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            roomno = 0
            for room in roomwisetoken:
                writer.writerow([rooms[roomno]])
                roomno += 1
                writer.writerow(['Handle', 'Name', 'ID', 'Semester', 'Section', 'Token', 'Tshirt_Size', 'PC'])
                for index, row in room.iterrows():
                    writer.writerow([str(room.loc[index].student_name)+'['+str(room.loc[index].vid)+ ', ' + str(room.loc[index].semester)+'-'+str(room.loc[index].section) +'](' + str(room.loc[index].token) + ')',
                    room.loc[index].student_name, 
                    room.loc[index].id, 
                    room.loc[index].semester, 
                    room.loc[index].section, 
                    room.loc[index].token, 
                    room.loc[index].tshirt, 
                    room.loc[index].pc])
    

    def sequential(self, rand, room, index):
        #there might be previous index might not be
        if int(index)>0:
            previousindex = index-1
            # print(type(previousindex), type(room.loc[previousindex].pc), previousindex, room.loc[previousindex].pc)
            if previousindex in room.index and (int(room.loc[previousindex].pc) == rand+1 or int(room.loc[previousindex].pc) == rand-1):                
                return True
            #same semester and section
            # if previousindex in room.index and room.loc[previousindex].semester == room.loc[index].semester and room.loc[previousindex].section == room.loc[index].section:                
            #     return True
        return False


    def shuffleseatarrangement(self, computernumber, roomwisetoken):
        print("Re-arranging seating arrangement")
        roomno = 1 
        for room in roomwisetoken:
            assigned = []
            print("Working on room: " + str(roomno))
            roomno += 1
            for index, row in room.iterrows():
                rand = random.randint(1, 35)
                sequencecount = 1
                while (room.loc[index].pc == None or room.loc[index].pc == '') or rand in assigned or self.sequential(rand, room, index):
                    sequencecount += 1
                    rand = random.randint(1, 35)
                print(index, 'pc', rand)             
                room.at[index, 'pc'] = int(rand)
                assigned.append(rand)

    def distributetoken(self, nocomputer, roomcount):
        print("Distributing students to room according to number of rooms and number of computer per room.")
        df = self.getdataframe()
        roomwisetoken = []
        for i in range(roomcount):
            room = df[df.token > i*nocomputer]
            room = room.loc[:(((i+1)*nocomputer)-1), :]
            roomwisetoken.append(room)
        return roomwisetoken


    def tshirtcountsave(self, roomwisetoken, rooms):
        print("Counting number of tshirt per room and save them.")
        with open('tshirtcount.csv', 'w+', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(['Room', 'S', 'M', 'L', 'XL', 'XXL', 'Total'])
            roomno = 0
            for room in roomwisetoken:
                writer.writerow([rooms[roomno], room.tshirt[room.tshirt == 'S'].count(),
                 room.tshirt[room.tshirt == 'M'].count(),
                 room.tshirt[room.tshirt == 'L'].count(),
                 room.tshirt[room.tshirt == 'XL'].count(),
                 room.tshirt[room.tshirt == 'XXL'].count(),
                 room.tshirt.count()])
                roomno += 1

    def saveseatplanrange(self, roomwisetoken, rooms):
        print("Saving seating range.")
        with open('seatrangeplan.csv', 'w+', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            roomno = 0
            writer.writerow(["Room", "From", "To"])
            for room in roomwisetoken:                                
                writer.writerow([rooms[roomno], room.iloc[0].token, room.iloc[-1].token])
                roomno += 1

    def getdataframe(self):
        return pd.DataFrame(self.dataframe)
    
    def get1stsemester(self):
        return pd.DataFrame(self.semester1)
    
    def get2ndsemester(self):
        return pd.DataFrame(self.semester2)

    def setdataframe(self, dataframe):
        self.dataframe = dataframe
    
    def set1stsemester(self, dataframe):
        self.semester1 = dataframe
    
    def set2ndsemester(self, dataframe):
        self.semester2 = dataframe