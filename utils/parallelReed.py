import time
import multiprocessing


class parallelReed():
    cores = 0  # TODO setze es auf einen standard wert, für den fall das es später nicht richtig geändert wird
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
        parallelReed.pool = multiprocessing.Pool(
            processes=(parallelReed.cores*4))

    def f(input_num, pos, return_dict):
        # TODO put here our function for decoding/encoding
        # input is a vector to change, output is the changed vector
        # pos and return_dict will stay the same, as well as our function to put it back together
        # give the function also the encoding object, so we don'T need to process it each time from the beginning (means the galois field)
        time.sleep(input_num % 3)
        # todo index wont work correct, so put it in the return vector itself and sort it then
        return_dict[pos] = [input_num*3, input_num*input_num, input_num*5]

    # array hat arrays als spalten gespeichert [[][][]]
    def encode(input_vec, inner, pos, return_dict):
        output_vec = []
        # encode input_vec using galoisField
        if(inner):
            for
        else:
        return_dict[pos] = output_vec

    def decode(input_vec, inner, pos, return_dict):
        output_vec = []
        # decode input_vec using galoisField
        return_dict[pos] = output_vec

    def startEncode(inputList):  # Input should be a list of arrays with arrays (594x30)
        start_time = time.time()  # start time

        # create manager/dict for return values
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        # start all new processes
        i = 0
        for block in inputList:
            parallelReed.pool.apply_async(
                func=parallelReed.encode, args=(block, i, return_dict))

        # stop the pool at the end
        parallelReed.pool.close()
        parallelReed.pool.join()

        result = []

        for i in range(len(return_dict)):
            result.append(return_dict.get(i))

        print(result)

        print("--- %s seconds ---" % (time.time() - start_time))

        # TODO result will be there as a list of arrays in arrays, needs to be convertet to string again

    # Input should be a list of arrays with arrays (713x39)
    def startRsCode(inputList, codeType, inner):
        start_time = time.time()  # start time

        # create manager/dict for return values
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        # start all new processes
        i = 0
        for block in inputList:
            if(codeType):  # encoding
                parallelReed.pool.apply_async(func=parallelReed.encode, args=(
                    block, inner, i, return_dict))
            else:  # decoding
                parallelReed.pool.apply_async(func=parallelReed.decode, args=(
                    block, inner, i, return_dict))

        # stop the pool at the end
        parallelReed.pool.close()
        parallelReed.pool.join()

        result = []

        print(len(return_dict))

        for i in range(len(return_dict)):
            result.append(return_dict.get(i))

        print(result)

        print("--- %s seconds ---" % (time.time() - start_time))

        # TODO result will be there as a list of arrays in arrays, needs to be convertet to string again
