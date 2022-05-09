

class sortBlock():
    def sortBubble(self, block):  # simple bubblesort
        print("Not yet implemented.")
        for i in range(0, len(block)):
            biggestValue = [0, 0, 0]
            biggestValueIndex = 0
            for z in range(0, (len(block) - i)):
                if(self.compare(block[z], biggestValue)):
                    biggestValue = block[z]
                    biggestValueIndex = z
            if(biggestValueIndex != ((len(block) - i) - 1)):
                temp = block[biggestValueIndex]
                block[biggestValueIndex] = block[((len(block) - i) - 1)]
                block[((len(block) - i) - 1)] = temp

    def compare(self, index1, index2):
        if(index1[0] == index2[0]):
            if(index1[1] == index2[1]):
                return index1[2] > index2[2]
            else:
                return index1[1] > index2[1]
        else:
            return index1[0] > index2[0]
