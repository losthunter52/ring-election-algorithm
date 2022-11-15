from bin.Data import Database
from bin.Core import Processor
from bin.Receptor import Receptor

# ---------------------------------------------------------------------------
# Main Class
# ---------------------------------------------------------------------------

# main method
def Main():
    # responsible for starting and ending the node
    data = Database()
    threads = []

    # init threads
    core = Processor(data)
    threads.append(core)
    core.start()
    receptor = Receptor(data)
    threads.append(receptor)
    receptor.start()

    # join threads
    for thread in threads:
        thread.join()


# program launcher
if __name__ == '__main__':
    Main()