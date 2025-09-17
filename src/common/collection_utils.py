def find_last_occurrence(collection, item):
    """ Without copying collection """
    for i, x in enumerate(reversed(collection)):
        if x == item:
            return len(collection) - 1 - i
    return -1
