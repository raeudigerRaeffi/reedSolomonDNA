class NumberSystemConversion():
    # C++ implementierung
    def tobase(nu, base, size):
        nn = []
        for x in range(size):
            nn.append(0)
        if(nu == 0):
            return nn

        div = nu
        i = 0
        while(div != 0 and i < size):
            nn[i] = int(div % base)
            div = int(div / base)
            i += 1

        return nn

    def frombase(nn, base):
        nu = 0
        basepow = 1
        for n in nn:
            nu += (n * basepow)
            basepow *= base

        return nu

    def char2pfe(data_char):
        output = []

        if((len(data_char) % 2) != 0):
            data_char.append(10)  # append \n

        for i in range(0, len(data_char), 2):
            indec = NumberSystemConversion.frombase(data_char[i:i+2], 256)
            tmpvec = NumberSystemConversion.tobase(indec, 47, 3)
            output.extend(tmpvec)

        return output

    def pfe2char(data_char):
        output = []

        if((len(data_char) % 3) != 0):
            return output

        for i in range(0, len(data_char), 3):
            indec = NumberSystemConversion.frombase(data_char[i:i+3], 47)
            tmpvec = NumberSystemConversion.tobase(indec, 256, 2)
            output.extend(tmpvec)

        return output
