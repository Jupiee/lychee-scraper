class Item:

    def __init__(self, *args):

        self.name = args[0]
        self.file_size= args[1]
        self.date_uploaded= args[2]
        self.platforms= args[3]
        self.download_links= args[4]
        self.thumbnail= None