import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.g = nx.DiGraph()
        self.mapNodi = {}
        self.soluzione = []

    def getStores(self):
        return DAO.getStores()

    def buildgraph(self, store, giorni):
        self.g.clear()
        self.mapNodi.clear()
        self.addnodes(store)
        self.addedges(store, giorni)
        return self.g

    def addnodes(self, store):
        for nodo in DAO.getNodi(store):
            self.mapNodi[nodo.order_id] = nodo
            self.g.add_node(nodo)

    def addedges(self, store, giorni):
        for arco in DAO.getArchi(store, giorni):
            p1 = self.mapNodi[arco[0]]
            p2 = self.mapNodi[arco[1]]
            self.g.add_edge(p1, p2, weight=arco[2])

    def getNodes(self):
        return list(self.g.nodes)

    def getNumNodes(self):
        return len(self.g.nodes)

    def getNumEdges(self):
        return len(self.g.edges)

    def getPercorsoMax(self, nodoid):
            source = self.mapNodi[nodoid]
            lp = []  # longest path

            tree = nx.dfs_tree(self.g, source) #dal mio grafo creo un albero di nodi a cui posso arrivare
            nodi = list(tree.nodes()) #lista di nodi raggiungibili compreso il primo

            for node in nodi: #li scorro
                tmp = [node] #per ogni nodo che posso raggiungere, lo inserisco nei temporanei
                while tmp[0] != source: #se sono già alla sorgente non mi interessa
                    pred = nx.predecessor(tree, source, tmp[0])
                    tmp.insert(0, pred[0])  # inserisce il predecessore in testa (costruisce il cammino)

                if len(tmp) > len(lp):
                    lp = copy.deepcopy(tmp)
            return lp

    def ricorsione(self, parziale, ultimo, visitati):
        if len(self.soluzione) <= len(parziale):
            self.soluzione = copy.deepcopy(parziale)

        for nodo in self.g.successors(ultimo):
            id_nodo = nodo.order_id
            if id_nodo not in visitati:
                parziale.append(id_nodo)
                visitati.add(id_nodo)
                self.ricorsione(parziale, nodo, visitati)
                parziale.pop()
                visitati.remove(id_nodo)


