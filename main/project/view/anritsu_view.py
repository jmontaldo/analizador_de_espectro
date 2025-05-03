import sys
import os
from subprocess import run
from tkinter import *
from tkinter import font, ttk, messagebox, filedialog

MODULES_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(MODULES_PATH)

from service.anritsu import SpectrumAnalizer, Parameters
from model.database import Registros

class ProgramView:
    def __init__(self):
        self.master = Tk()
        self.master.geometry("510x310")
        self.master.title("Analizador de espectro Express")

        #Configuracion general
        self.font = font.Font(font="Arial", size=10)

        #Variables
        self.radio_var = StringVar()
        self.radio_var.set(None)
        self.frecuency = IntVar()
        self.lnb = IntVar()
        self.symbol = DoubleVar()
        self.search_var = StringVar()
        self.plot_name = StringVar()

        #Contenedor principal
        self.main_container = Frame(self.master)
        self.main_container.grid(column=0, row=0, padx=15, pady=2, sticky=W)

        #Contenedor del formulario: 'Datos'
        self.data_container = Frame(self.main_container)
        self.data_container.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        #Formulario 'Datos'
        self.freq_label = Label(self.data_container, text="Frecuencia", font=self.font)
        self.freq_label.grid(column=0, row=0, padx=5, pady=5)

        self.freq_input = Entry(self.data_container, textvariable=self.frecuency, width=10, font=self.font)
        self.freq_input.grid(column=1, row=0, padx=5, pady=5)

        self.lnb_label = Label(self.data_container, text="LNB", font=self.font)
        self.lnb_label.grid(column=0, row=1, padx=5, pady=5)

        self.lnb_list = [10750, 10500, 5150]
        self.question_menu = OptionMenu(self.data_container, self.lnb, *self.lnb_list)
        self.question_menu.configure(border=1, relief=SUNKEN, width=6, font=self.font, anchor=W, bg="#FFFFFF")
        self.lnb.set(self.lnb_list[2]) #Poniendo la opción por defecto en 5150 MHz
        self.question_menu.grid(column=1 ,row=1, padx=5, pady=5)

        self.symbol_label = Label(self.data_container, text="Symbol Rate", font=self.font)
        self.symbol_label.grid(column=0, row=2, padx=5, pady=5)

        self.symbol_input = Entry(self.data_container, textvariable=self.symbol, width=10, font=self.font)
        self.symbol_input.grid(column=1, row=2)

        #Contenedor del formulario - Modos
        self.mode_container = Frame(self.main_container)
        self.mode_container.grid(column=1, row=0, padx=15, pady=5, sticky=N)

        #Botonera de modos
        self.radio_normal = Radiobutton(self.mode_container, text="Normal", variable=self.radio_var,
            value="trac1:type NORM;:init:cont 1", font=self.font)
        self.radio_normal.grid(column=0, row=0, sticky=W)

        self.radio_max = Radiobutton(self.mode_container, text="MaxHld",  variable=self.radio_var, 
            value="trac1:type MAX", font=self.font)
        self.radio_max.grid(column=0, row=1, sticky=W)

        self.radio_min = Radiobutton(self.mode_container, text="MinHld", variable=self.radio_var,
            value="trac1:type MIN", font=self.font)
        self.radio_min.grid(column=0, row=2, sticky=W)

        self.radio_freeze = Radiobutton(self.mode_container, text="Freeze", variable=self.radio_var,
            value="init:cont 0", font=self.font)
        self.radio_freeze.grid(column=0, row=3, sticky=W)

        #Contenedor de botones
        self.button_container = Frame(self.main_container)
        self.button_container.grid(column=2, row=0, padx=10, pady=5, sticky=NE)

        #Botones
        self.upload_button = Button(self.button_container, text="Cargar", 
            command=lambda: self.send_frecuency_data(self.frecuency, self.lnb, self.symbol, False), 
            font=self.font, width=12
        )
        self.upload_button.grid(column=0, row=1, padx=5, pady=5)

        self.mode_button = Button(self.button_container, text="Cambiar Modo", 
            command=lambda: self.send_modes(self.radio_var), font=self.font, width=12)
        self.mode_button.grid(column=0, row=2, padx=5, pady=5)

        self.plot_button = Button(self.button_container, text="Plotear",
            command=lambda: self.send_frecuency_data(self.frecuency, self.lnb, self.symbol, True),
            font=self.font, width=12
        )
        self.plot_button.grid(column=0, row=3, padx=5, pady=5)

        #Contenedor de base de datos
        self.base_container = Frame(self.master, bd=3, relief=RIDGE)
        self.base_container.grid(column=0, row=1, padx=5, pady=5)

        #Contenedor de busqueda
        self.search_container = Frame(self.base_container, bd=2, relief=FLAT)
        self.search_container.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        #Buscar
        self.search_label = Label(self.search_container, text="Señal", font=self.font)
        self.search_label.grid(column=0, row=0, padx=5, pady=5)

        self.search_entry = Entry(self.search_container, textvariable=self.search_var, font=self.font)
        self.search_entry.grid(column=1, row=0, padx=5, pady=5)

        self.search_button = Button(self.search_container, text="Buscar", 
            command=lambda: self.search(self.search_var), font=self.font)
        self.search_button.grid(column=2, row=0, padx=5)

        #Boton seleccionar
        self.select_button = Button(self.base_container, text="Seleccionar", command=lambda: self.load_data(),
            width=12, font=self.font)
        self.select_button.grid(column=1, row=0, padx=5, pady=5)

        #Treeview
        self.tree = ttk.Treeview(self.base_container)
        self.tree["columns"] = ("col1", "col2", "col3")
        self.tree.column("#0", width=200, minwidth=150)
        self.tree.heading("#0", text="Feed")
        self.tree.column("col1", width=100, minwidth=40)
        self.tree.heading("col1", text="Satelite")
        self.tree.column("col2", width=80, minwidth=40)
        self.tree.heading("col2", text="Frecuencia")
        self.tree.column("col3", width=80, minwidth=40)
        self.tree.heading("col3", text="Symbol Rate")
        self.tree.configure(height=3)
        self.tree.grid(column=0, row=1, padx=5, pady=10, sticky=W, columnspan=2)

        #scrollbar
        self.scrollbar = ttk.Scrollbar(self.base_container, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(column=2, row=1)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        #Menu desplegable
        self.menu = Menu(self.master)
        self.barra_menu = Menu(self.menu, tearoff=0)
        self.barra_menu.add_command(label="Abrir", command=lambda: self.load_file())
        self.menu.add_cascade(label="Archivo", menu=self.barra_menu)

        #Agregar el menu
        self.master.config(menu=self.menu)

        #Correr la vista
        self.master.mainloop()

    def send_frecuency_data(self, frc, lnb, symbol, flag):
        try:
            frecuencia = frc.get()
            lnb = lnb.get()
            symbol = symbol.get()
        except TclError:
            messagebox.showinfo(title="Ingreso no valido!", message="Los valores ingresados deben ser números!")
        else:
            params = Parameters(frecuencia, lnb, symbol)
            params.set_frecuency()
            if flag == False:
                cmd = f"SENS:FREQ:CENT {params.lband} MHZ;:SENS:FREQ:SPAN {params.symbol * 5} MHz"
                params.send_command(cmd, messagebox)
            else:
                self.ventana_save_plot()
                params.plot_carrier(messagebox, self.plot_name.get())

    def send_modes(self, mode):
        SpectrumAnalizer().send_command(mode.get(), messagebox)

    def search(self, sn):
        signal = sn.get()
        flag = Registros.search(signal, self.tree, messagebox)

    def load_data(self):
        item = self.tree.focus()
        self.frecuency.set(self.tree.item(item)["values"][1])
        self.symbol.set(self.tree.item(item)["values"][2])

    def ventana_save_plot(self):
        self.ventana = Toplevel(self.master)
        self.ventana.title("Guardar ploteo")
        self.ventana.geometry("330x50")
        self.save_label = Label(self.ventana, text="Nombre del archivo")
        self.save_label.grid(column=0, row=0, padx=5, pady=5)
        self.save_entry = Entry(self.ventana, textvariable=self.plot_name)
        self.save_entry.grid(column=1, row=0, padx=5, pady=5)
        self.save_button = Button(self.ventana, text="Guardar", command=lambda: self.save_file())
        self.save_button.grid(column=2, row=0, padx=5, pady=5)
        self.master.wait_window(self.ventana)

    def save_file(self):
        file_name = self.plot_name.get()
        self.plot_name.set(file_name)
        self.ventana.destroy()
    
    def load_file(self):
        selected_file = filedialog.askopenfile(title="Seleccione un archivo",
            filetypes=[("Archivo json", "*json")])
        if selected_file:
            self.graficar(selected_file.name)
    
    def graficar(self, file_path):
        upperdir = os.path.dirname(os.path.dirname(file_path))
        exec_path = os.path.join(upperdir, "plotter.py")
        run([sys.executable, exec_path, file_path])