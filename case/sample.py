import logging
def add(**kwargs):
    a = int(kwargs["a"])
    b = int(kwargs["b"])
    logging.info("%d + %d = %d" % (a, b, a + b))
    return a + b
