# ---------------------------------------------------------------------------
# Database Class
# ---------------------------------------------------------------------------

class Database:
    # init method
    def __init__(self):
        # initializes the database struct
        self.list = []

    # addJson method
    def addJson(self, json):
        # add a json to the database
        self.list.append(json)

    # clearList method
    def clearList(self):
        # clear the json list
        self.list.clear()

    # get method
    def getJson(self):
        # return the json objects and clear the queue
        if len(self.list) > 0:
            aux = self.list[0]
            self.list.pop(0)
            return aux
        else:
            return 'NULL'