class NXSound:

    def __init__(self, nxfile, offset):
        self.nxfile = nxfile
        self.offset = offset

    def get_data(self, length):
        """ Get sound data """
        self.nxfile.file.seek(self.offset)
        return self.nxfile.file.read(length)
