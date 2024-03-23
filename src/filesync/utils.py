def safeListGet(l: list, i: int, d=None):
    try:
        e = l[i]
    except IndexError:
        e = d
    return e