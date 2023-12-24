class Item:

    def __init__(self, *args):

        self.name = args[0]
        self.file_size= args[1]
        self.platforms= args[2]
        self.download_links= args[3]