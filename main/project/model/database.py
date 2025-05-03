import os
import csv

class DataBase():

    file = os.path.dirname(os.path.abspath(__file__)) + "\SatelliteDelivery.csv"

    def __repr__(cls):
        return f"Base de datos: {cls.file}"
    
class Registros(DataBase):
    
    @classmethod
    def search(cls, signal, treeview, msgbx):
        flg = False # Control if there's coincidence in the registers with the value
        signal = signal[0].upper() + signal[1:]
        treeview.delete(*treeview.get_children())   #Clearing the tree
        with open(cls.file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if signal in row["Feed"]:
                    treeview.insert("", "end", text=str(row["Feed"]),
                        values=(row["Downlink Satellite"], row["Frequency-C"], row["Symbol Rate"]))
                    flg = True     
        if not flg:  
            msgbx.showinfo(title="¡No encontrado!", 
                message=f"No se han encontrado coincidencias con '{signal}'. ¡Intente nuevamente!"
            )