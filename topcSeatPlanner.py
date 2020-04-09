import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import csv
import random

class arrange:
    def __init__(self, filepath = "topc_reg.csv"):
        self.filepath = filepath
        self.dataframe = pd.read_csv(filepath)
        self.dataframeDict = self.dataframe.to_dict()
        self.rooms = [601, 602, 701, 801, 802, 901, 902, 903, 702]
        self.planSeat(minimumPc = 33, rooms = self.rooms)

    def planSeat(self, minimumPc, rooms):
        print("Processing Data.. ")
        self.saveseatplanrange(minimumPc, rooms)
        self.savetshirtcount(rooms)
        self.shuffleseatarrangement(rooms)
        self.saveseatplanindividual(rooms)
        self.savelogincredentials(rooms)


    def checkValidityScore(self, ids):
        score = 0
        for i in range(len(ids)):
            if not i:
                continue
            now = ids[i]
            prv = ids[i-1]

            if( self.dataframeDict['section'][now] == self.dataframeDict['section'][prv] and
                self.dataframeDict['semester'][now] == self.dataframeDict['semester'][prv] and
                self.dataframeDict['department'][now] == self.dataframeDict['department'][prv]):
                score += 1
        return score

    def shuffleseatarrangement(self, rooms):
        print("Shuffling seats...")
        roomno = 0
        self.score = dict()
        self.seats = dict()
        for room in rooms:
            ranges = self.roomRanges[roomno]
            self.seats[roomno] = [x for x in range(ranges[0], ranges[1] + 1)]
            tmp = self.seats[roomno]
            score = self.checkValidityScore(tmp)

            for _ in range(100000):
                random.shuffle(tmp)
                tmpScore = self.checkValidityScore(tmp)
                if(tmpScore <  score):
                    score = tmpScore
                    self.seats[roomno] = list(tmp)
            print("Room ", room, "done", " Validity Score:", score)
            if(self.checkValidityScore(self.seats[roomno]) != score):
                print(roomno, "Milchhena")
            self.score[roomno] = score
            roomno += 1

    def saveseatplanindividual(self, rooms):
        print("Saving seatplan for rooms.")
        with open('seatplan.csv', 'w+', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            roomno = 0
            dfd = self.dataframeDict
            for room in rooms:
                writer.writerow([rooms[roomno], dfd['token'][self.roomRanges[roomno][0]], dfd['token'][self.roomRanges[roomno][1]], self.score[roomno]]) # roomname, token range, matchscore
                writer.writerow(['Token', 'Name', 'Tshirt_Size', 'PC'])

                ranges = self.roomRanges[roomno]
                pcNo = 1
                for x in self.seats[roomno]:
                    writer.writerow([
                        dfd['token'][x],
                        str(dfd['student_name'][x]) + ' [' + str(dfd['vid'][x]) + ', ' + str(dfd['semester'][x]) + '-' + str(dfd['section'][x]) + ', ' + str(dfd['department'][x]) + ']',
                        dfd['tshirt'][x] if (type(dfd['tshirt'][x])  == str) else "--",
                        pcNo
                    ])
                    pcNo += 1

                roomno += 1

    def savelogincredentials(self, rooms):
        print("Saving login credentials for rooms.")
        with open('logincredentials.csv', 'w+', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            roomno = 0
            dfd = self.dataframeDict
            for room in rooms:
                writer.writerow([rooms[roomno], dfd['token'][self.roomRanges[roomno][0]], dfd['token'][self.roomRanges[roomno][1]]]) # roomname, token range, matchscore
                writer.writerow(['PC', 'Name', 'Handle', 'Password'])

                ranges = self.roomRanges[roomno]
                pcNo = 1
                for x in self.seats[roomno]:
                    writer.writerow([
                        pcNo,
                        dfd['name'][x],
                        dfd['handle'][x],
                        dfd['password'][x]
                    ])
                    pcNo += 1

                roomno += 1

    def savetshirtcount(self, rooms):
        print("Counting number of tshirt per room and save them.")
        with open('tshirtcount.csv', 'w+', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(['Room', 'S', 'M', 'L', 'XL', 'XXL', '3XL', 'None', 'Total'])
            roomno = 0
            for room in rooms:
                ranges = self.roomRanges[roomno]
                tShirtData = [self.dataframeDict['tshirt'][idx] for idx in range(ranges[0], ranges[1]+1)]
                writer.writerow([rooms[roomno],
                    tShirtData.count('S'),
                    tShirtData.count('M'),
                    tShirtData.count('L'),
                    tShirtData.count('XL'),
                    tShirtData.count('XXL'),
                    tShirtData.count('3XL'),
                    tShirtData.count(np.nan),
                    len(tShirtData)])
                roomno += 1

    def saveseatplanrange(self, pcCount, rooms):
        print("Saving seating range.")
        self.roomRanges = dict()
        with open('seatrangeplan.csv', 'w+', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            roomno = 0
            writer.writerow(["Room", "From", "To", "Total"])
            for room in rooms:
                start = roomno*pcCount
                end = min((roomno+1)*pcCount, len(self.dataframeDict['token'])) - 1
                self.roomRanges[roomno] = (start, end)
                if(start >= len(self.dataframeDict['token'])):
                    writer.writerow([rooms[roomno], "-", "-", "-"])    
                else:
                    writer.writerow([rooms[roomno], self.dataframeDict['token'][start], self.dataframeDict['token'][end], end - start + 1])
                roomno += 1
        print(self.roomRanges)