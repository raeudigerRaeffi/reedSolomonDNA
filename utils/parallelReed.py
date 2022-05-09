import time
import multiprocessing
import sortBlock


class parallelReed():
    cores = 8
    pool = None
    inner_encoder = None
    outer_encoder = None

    def __init__(self, inner_encoder, outer_encoder):
        self.inner_encoder = inner_encoder
        self.outer_encoder = outer_encoder
        # Count number of cpu cores
        parallelReed.cores = multiprocessing.cpu_count()
        print(parallelReed.cores)

        # create Pool
        self.pool = multiprocessing.Pool(
            processes=(parallelReed.cores*4))

    def encode(input_vec, encoder, pos, return_dict):
        output_vec = encoder.encode(input_vec)
        return_dict[pos] = output_vec

    def decode(input_vec, decoder, pos, return_dict):
        output_vec = decoder.decode(input_vec)
        return_dict[pos] = output_vec

    # Input should be a list of arrays with array-size (713x39)
    def startRsCode(self, inputList, codingType):
        start_time = time.time()  # TODO remove the time
        index = [0, 0, 0]

        # create manager/dict for return values
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        if(codingType == 0):
            print("Encode")
            for block in inputList:
                # Convert Data to 1 dimensional arrays
                for y in range(3, 34):  # outer encode dataStrings
                    dataString = []

                    for x in range(119, 713):
                        dataString.append(block[x][y])

                    self.pool.apply_async(func=parallelReed.encode, args=(
                        dataString, self.outer_encoder, (y - 3), return_dict))

                # stop the pool at the end
                self.pool.close()
                self.pool.join()

                # write back the outer data
                for y in range(3, (len(return_dict) + 3)):
                    encodedData = return_dict.get((y - 3))
                    for x in range(0, 119):  # 0-593 (message) => 594-712 (encoding data)
                        block[x][y] = encodedData[(x + 594)]
                return_dict.clear()

                # add the index
                for x in range(0, 713):
                    for y in range(0, 3):
                        block[x][y] = index[y]

                    increaseIndex(index)

                # encode inner data
                for x in range(0, 713):
                    self.pool.apply_async(func=parallelReed.encode, args=(
                        block[x][0:32], self.inner_encoder, x, return_dict))

                # stop the pool at the end
                self.pool.close()
                self.pool.join()

                # write back the inner data
                for x in range(0, len(return_dict)):
                    encodedData = return_dict.get(x)
                    for y in range(33, 39):  # 0-32 (message) => 33-38 (encoding data)
                        block[x][y] = encodedData[y]
                return_dict.clear()
        else:
            print("Decode")
            for block in inputList:
                # encode inner data
                for x in range(0, 713):
                    self.pool.apply_async(func=parallelReed.decode, args=(
                        block[x][0:38], self.inner_encoder, x, return_dict))

                # stop the pool at the end
                self.pool.close()
                self.pool.join()

                # write back the inner data
                for x in range(0, len(return_dict)):
                    decodedData = return_dict.get(x)
                    for y in range(0, 33):
                        block[x][y] = decodedData[y]
                return_dict.clear()

                # sort data with index
                sort = sortBlock()
                sort.sortBubble(block)

                # Convert Data to 1 dimensional arrays (should be sortet by now after index)
                for y in range(3, 33):  # outer decode dataStrings
                    dataString = []

                    for x in range(0, 713):
                        dataString.append(block[x][y])

                    self.pool.apply_async(func=parallelReed.decode, args=(
                        dataString, self.outer_encoder, (y - 3), return_dict))

                # stop the pool at the end
                self.pool.close()
                self.pool.join()

                # write back the outer data
                for y in range(3, (len(return_dict) + 3)):
                    encodedData = return_dict.get((y - 3))
                    for x in range(119, 713):
                        block[x][y] = encodedData[(x - 119)]
                return_dict.clear()

        print("--- %s seconds ---" %
              (time.time() - start_time))  # TODO remove the time

        return inputList  # TODO test without return


def increaseIndex(index):
    index[2] += 1
    if(index[2] >= 47):
        index[2] = 0
        index[1] += 1
        if(index[1] >= 47):
            index[1] = 0
            index[0] += 1
            if(index[0] >= 47):
                index[2] = 0
                index[1] = 0
                index[0] = 0
                # TODO find solution to this?
                print("Index was to big, got resettet.")
