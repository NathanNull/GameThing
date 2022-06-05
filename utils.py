def add(*tuples):
    for i in range(len(tuples)):
        if len(tuples[i]) != len(tuples[max(0, i-1)]):
            raise ValueError("Tuples are not the same length")

    return tuple([sum(v) for v in zip(*tuples)])