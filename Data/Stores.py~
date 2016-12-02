from Data.Nodes import Node, Network

class Store:
    #Stores are the interface to persistent imprints of gorg networks.  A single Store is linked to a single Network.

    def getnetwork(self):
        raise NotImplementedError        

    def writenetwork(self):
        raise NotImplementedError

class JSONStore(Store):

    def __init__(self, file_path):
        # Accepts as argument a filepath to a json file in which a Network is stored.  Returns a JSONStore object.
        self._path = file_path

    def getnetwork(self):
        import json
        store_file = open(self._path, "r")
        node_dict = json.load(store_file) #networks are stored in json as dictionaries, with index numbers as the key, and a second dictionary of node properties as the value.
        nodes_list = []
        for node_index in node_dict:
            nodes_list.append(Node(index=node_index, 
                                       properties=node_dict[node_index]))
        network = Network(nodes=nodes_list)
        return network

    def writenetwork(self, network):
        import json
        store_file = open(self._path, "w")
        nodes_dict = {}
        for node in network.getnodes():
            nodes_dict.update({node.getindex(): node.getprops()})
        json.dump(nodes_dict, store_file)
        
class StoreHouse:

    def getlast(self):
        raise NotImplementedError

    def store(self, network):
        raise NotImplementedError

class JSONDir(StoreHouse):

    def __init__(self, directory_path):
        self._dir_path = directory_path

    def _makelast(self):
        import os
        file_names = os.listdir(self._dir_path)
        file_names.remove(".DS_Store")
        dates_list = []
        for i in file_names:
            file_date = int((i.partition("gorg-")[2].partition(".txt")[0]))
            dates_list.append(file_date)
        last_date = max(dates_list)
        target_file_name = "gorg-" + str(last_date) + ".txt"
        target_file_path = self._dir_path + target_file_name
        return JSONStore(target_file_path)

    def getlast(self):
        return self._makelast().getnetwork()
        
    def store(self, network):
        import time
        now = time.localtime()
        time_list = [str(i) for i in now] # now is a 'struct time' obj, which is an iter
        time_list[0] = time_list[0][2:] # truncating yyyy to yy
        for i in range(len(time_list)):
            if len(time_list[i]) == 1:
                time_list[i] = ''.join(['0', time_list[i]])
        time_string = ''.join(time_list[:6])
        file_name = "gorg-" + time_string + ".txt"
        file_path = self._dir_path + file_name
        store = JSONStore(file_path)
        store.writenetwork(network)
            
