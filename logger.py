class Logger:

    _file = None
    
    @staticmethod
    def init(fileName):
        Logger._file = open(fileName, "w")

    @staticmethod
    def close():
        Logger._file.close()

    @staticmethod
    def write(msg):
        Logger._file.write(str(msg))