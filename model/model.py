import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()
        self.id_art_map={}
        for artist in self._artists_list:
            self.id_art_map[artist.id] = artist
        self.nodes=[]

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        return DAO.get_all_nodes(min_albums,self.id_art_map)


    def build_graph(self,min_albums):
        self.nodes=self.load_artists_with_min_albums(min_albums)
        self._graph.add_nodes_from(self.nodes)
        connessioni=DAO.get_connessioni(min_albums)
        for c in connessioni:
            a1=self.id_art_map[c.a1_id]
            a2=self.id_art_map[c.a2_id]
            self._graph.add_edge(a1,a2,weight=c.generi)

    def get_graph_details(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()
    def get_nodes(self):
        return self._graph.nodes()
    def get_edges(self):
        return self._graph.edges()
    def get_component(self,artist):
        if artist not in self._graph.nodes():
            return []
        connected= list(nx.connected_components(self._graph,artist))
        return connected.sort(key=lambda x: x.id)





