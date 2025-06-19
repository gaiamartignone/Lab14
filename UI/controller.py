import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.view = view
        # the model, which implements the logic of the program and holds the data
        self.model = model
        self.liststores = self.model.getStores()
        self.currentStore = None
        self.currentNodo = None

    def fillDD_stores(self):
        for s in self.liststores:
            self.view._ddStore.options.append(ft.dropdown.Option(text=s,
                                                                  data=s,
                                                                  on_click=self.read_DD_Stato))
        self.view.update_page()

    def read_DD_Stato(self, e):
        print("read_DD_Stato called ")
        if e.control.data is None:
            self.currentStore = None
        else:
            self.currentStore = e.control.data  # in questo modo ora ho l’oggetto che inserisco in data
        print(self.currentStore)

    def handleCreaGrafo(self, e):
        self.view.txt_result.controls.clear()
        #  controlli
        giorni = self.view._txtIntK.value
        store = self.currentStore
        if giorni is None or giorni == "":
            self.view.create_alert("Inserire un anno")
            return
        if store is None:
            self.view.create_alert("selezionare uno store")
            return

        try:
            giorni_int = int(giorni)
            # print nodi
            self.model.buildgraph(store,giorni_int)
            self.view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
            self.view.txt_result.controls.append( ft.Text(f"Numero di nodi: {self.model.getNumNodes()} \nNumero di archi: {self.model.getNumEdges()} "))

            # abilitazione e disabilitazione altri comandi
            self.view._btnCerca.disabled = False
            self.view._ddNode.disabled = False
            self.fillDD_nodi()
            self.view._btnRicorsione.disabled = False
            # update pagina
            self.view.update_page()
        except ValueError:
            self.view.create_alert("i giorni devono esser un numero intero")
            return

    def fillDD_nodi(self):
        for nodi in self.model.getNodes():
            self.view._ddNode.options.append(ft.dropdown.Option(text=nodi.order_id,
                                                                 data=nodi.order_id,
                                                                 on_click=self.read_DD_nodo))
            self.view.update_page()

    def read_DD_nodo(self, e):
        print("read_DD_Stato called ")
        if e.control.data is None:
            self.currentNodo= None
        else:
            self.currentNodo = e.control.data  # in questo modo ora ho l’oggetto che inserisco in data
        print(self.currentNodo)


    def handleCerca(self, e):
        print("eccomi")
        nodoid = self.currentNodo
        if nodoid is None:
            self.view.create_alert("selezionare uno store")
            return
        lista = self.model.getPercorsoMax(nodoid)
        self.view.txt_result.controls.append(
            ft.Text(f"Nodo di partenza: {lista[0].order_id} "))
        for nodo in lista[1:]:
            self.view.txt_result.controls.append(
                ft.Text(f"{nodo.order_id}"))
        self.view.update_page()

    def handleRicorsione(self, e):
        pass
