def add(**kwargs):
    a = int(kwargs["a"])
    b = int(kwargs["b"])
    print("%d + %d = %d"%(a,b,a+b))
    return True