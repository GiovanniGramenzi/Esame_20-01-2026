import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            min_a=int(self._view.txtNumAlbumMin.value)
        except ValueError:
            self._view.alert("Inserire un numero")
            return
        if min_a < 0:
            self._view.alert("Inserire un numero >0")
            return
        self._view.txt_result.controls.clear()
        self._model.build_graph(min_a)
        n_nodi,n_archi=self._model.get_graph_details()
        self._view.txt_result.controls.append(ft.Text(f'Grafo creato: {n_nodi} nodi, {n_archi} archi'))
        self.popola_dd_artisti()
        self._view.update_page()

    def popola_dd_artisti(self):
        self._view.ddArtist.controls.clear()
        self._view.ddArtist.options.disabled = False
        for a in self._model.get_nodes():
            self._view.ddArtist.options.append(ft.dropdown.Option(a))
        self._view.update_page()


    def handle_connected_artists(self, e):
        artist=self._view.ddArtist.value
        connected=self._model.get_component(artist)
        self._view.txt_result.controls.clear()
        for a in connected:
            self._view.txt_result.controls.append(ft.Text(f'{a}-numero di generi in comune{self._model._graph[artist][a]['weight']}'))
        self._view.update_page()




