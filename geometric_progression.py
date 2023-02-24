from collections.abc import Sequence

def identify_geometric_progression(sequence):
    """
    Determine if a sequence is a geometric progression.
    """
    assert isinstance(sequence, Sequence) & (not isinstance(sequence, str)), "Expect input to be a sequence that's not string"
    assert len(sequence) > 2, "Expect a sequence with more than 2 items"
    try:
        ratio = sequence[1]/sequence[0]
    except ZeroDivisionError:
        return False

    for i in range(1, len(sequence)):
        if sequence[i]/sequence[i-1] != ratio:
            return False
    return True


# Unit test
assert identify_geometric_progression([1, 2, 3, 4, 5]) == False
assert identify_geometric_progression([1.1, 2.2, 4.4, 8.8]) == True
assert identify_geometric_progression([1, 3, 4, 12]) == False
assert identify_geometric_progression([0, 2, 4]) == False
