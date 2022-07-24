import time
import multiprocessing
import utils.sortBlock as sortBlock


class parallelReed():
    # cores = 8
    # pool = None
    inner_encoder = None
    outer_encoder = None

    def __init__(self, inner_encoder, outer_encoder):
        self.inner_encoder = inner_encoder
        self.outer_encoder = outer_encoder
        # Count number of cpu cores
        # parallelReed.cores = multiprocessing.cpu_count()

        # create Pool
        # self.pool = multiprocessing.Pool(
        #    processes=(parallelReed.cores*4))

    def encodeInner(input_vec, encoder, pos, return_dict):
        output_vec = encoder.encode(input_vec)
        return_dict[pos] = output_vec

    def encodeOuter(input_vec, encoder, pos, return_dict):
        output_vec = encoder.encode(encoder.convert_to_symbol_array(input_vec))
        return_dict[pos] = encoder.symbol_array_to_array(output_vec)

    def decodeInner(input_vec, decoder, pos, return_dict):
        output_vec = decoder.decode(input_vec)
        return_dict[pos] = output_vec

    def decodeOuter(input_vec, decoder, pos, return_dict):
        output_vec = decoder.decode(decoder.convert_to_symbol_array(input_vec))
        return_dict[pos] = decoder.symbol_array_to_array(output_vec)

    # Input should be a list of arrays with array-size (713x39)
    def startRsCode(self, inputList, codingType):
        start_time = time.time()  # TODO remove the time

        # create manager/dict for return values
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        if(codingType == 0):
            # start outer encode
            for x, block in enumerate(inputList):
                parallelReed.encodeOuter(
                    block[119:713, 3:33].tolist(), self.outer_encoder, x, return_dict)
                # self.pool.apply_async(func=parallelReed.encodeOuter, args=(
                #    block[119:713, 3:33], self.outer_encoder, x, return_dict))

            # stop the pool at the end
            # self.pool.close()
            # self.pool.join()

            # fill in results
            for x, block in enumerate(inputList):
                block[0:119, 3:33] = return_dict.get(x)[594:713]

            return_dict.clear()

            # add the index
            index = [0, 0, 0]
            for block in inputList:
                for column in block:
                    for y in range(0, 3):
                        column[y] = index[y]

                    increaseIndex(index)

            # start inner encode
            for x, block in enumerate(inputList):
                for y, column in enumerate(block):
                    parallelReed.encodeInner(
                        column[0:33].tolist(), self.inner_encoder, ((x * 713) + y), return_dict)
                    # self.pool.apply_async(func=parallelReed.encodeInner, args=(
                    #    column, self.inner_encoder, x, return_dict))

            # stop the pool at the end
            # self.pool.close()
            # self.pool.join()

            # fill in results
            for x, block in enumerate(inputList):
                for y, column in enumerate(block):
                    column[33:39] = return_dict.get((x * 713) + y)[33:39]

            return_dict.clear()
        else:
            # start inner decode
            for x, block in enumerate(inputList):
                for y, column in enumerate(block):
                    print(((x * 713) + y))
                    print(column.tolist())
                    parallelReed.decodeInner(
                        column.tolist(), self.inner_encoder, ((x * 713) + y), return_dict)
                    # self.pool.apply_async(func=parallelReed.decodeInner, args=(
                    #    column, self.inner_encoder, x, return_dict))

            # stop the pool at the end
            # self.pool.close()
            # self.pool.join()

            # fill in results
            for x, block in enumerate(inputList):
                print(block[0:713, 0:33])
                for y, column in enumerate(block):
                    column[0:33] = return_dict.get((x * 713) + y)
                print(block[0:713, 0:33])

            return_dict.clear()

            # sort columns
            # 1. create new blocks

            # doppelte einfach abspeichern und in leere plätze einfügen

            # 2. put in columns on correct spot (sort & delete)
            # 3. save doubled data
            # 4. check if we can remove empty blocks (at the end)

            # TODO change inputList with the new createt list

            # start outer decode
            for x, block in enumerate(inputList):
                print(block[0:713, 3:33])
                parallelReed.decodeOuter(
                    block[0:713, 3:33].tolist(), self.outer_encoder, x, return_dict)
                # self.pool.apply_async(func=parallelReed.encodeOuter, args=(
                #    block[119:713, 3:33], self.outer_encoder, x, return_dict))

            # stop the pool at the end
            # self.pool.close()
            # self.pool.join()

            # fill in results
            for x, block in enumerate(inputList):
                block[119:713, 3:33] = return_dict.get(x)
                print(return_dict.get(x))
                print(block[119:713, 3:33])
                # pos = 0
                # for y in range(594, 713):
                #    block[pos, 3:33] = return_dict.get(x)[y]
                #    pos += 1

            return_dict.clear()

            # answer is in new list of arrays

            '''
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
                '''

        print("--- %s seconds ---" %
              (time.time() - start_time))  # TODO remove the time

        # return inputList  # TODO test without return # return nothing, because we work directly on the array


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
