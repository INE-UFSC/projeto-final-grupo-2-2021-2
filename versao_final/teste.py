def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class Teste:
    __X = 5

    def __init__(self) -> None:
        print(Teste.__X)


teste = Teste()
teste = Teste()
