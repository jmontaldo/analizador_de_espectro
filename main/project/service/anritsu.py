import socket
import os
import json
import time
from datetime import datetime

def commands_logs(func):
    def wrapper(*args):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), r"logs\logs.txt")
        with open(path, "a") as f:
            f.write(f"{datetime.now()} - {func.__name__}: {args[1]}\n")
        data = func(*args)
        return data
    return wrapper

class SpectrumAnalizer():

    ip_address=" " #The IP of your Spectrum analyzer goes here.
    port=9001   #Default port

    @classmethod
    @commands_logs
    def send_command(cls, command, msgbx, flag=False):

        """This method send the SCPI commands for the Spectrum Analizer and receive data from it"""

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((cls.ip_address, cls.port))
            s.settimeout(5)
            s.send((command + "\n").encode("utf-8"))
            if flag == True:
                time.sleep(2)
                data = s.recv(4096).decode()
                s.close()
                return data
            else:
                s.close()
                return None

        except ConnectionError:
            msgbx.showerror(title="Error de conexión", 
                message="Ha ocurrido un error al intentar establecer la conexión, intente nuevamente."
            )
            return None

        except TimeoutError:
            msgbx.showerror(title="Error de TimeOut", 
                message="Se ha agotado el tiempo de espera y el servidor no ha respondido. Intente nuevamente."
            )
            return None

class FrecuencyDescriptor():

    "** Validate the frecuency input. This value must be inside of the margins of C or Ku band **"

    def __get__(self, instance, owner):
        if instance._frecuency < 3400 or instance._frecuency > 12700:
            raise ValueError("La frecuencia debe ser un valor entre 3400 y 12700 MHz")
        else:
            return instance._frecuency

    def __set__(self, instance, value):
        if value < 3400 or value > 12700:
            raise ValueError("La frecuencia debe ser un valor entre 3400 y 12700 MHz")
        else:
            instance._frecuency = value
    
    def __delete__(self, instance):
        del instance._frecuency

class Parameters(SpectrumAnalizer):

    def __init__(self, frecuency, lnb, symbol):
        self._frecuency = frecuency
        self.lnb = lnb
        self.symbol = symbol
        self.lband = None

    frecuency = FrecuencyDescriptor()

    def set_frecuency(self):

        """Sets the convertion from C or ku band to L band frecuency"""

        if (self.frecuency - self.lnb) < 0:
            self.lband = (self.frecuency - self.lnb) * (-1)
        else:
            self.lband = self.frecuency - self.lnb

    def plot_carrier(self, msgbx, file_name):

        """Receive an array with the power level data from de Spectrum Analizer and then calculate
           the frecuency data using the display point count (in this case 515) and the span, then
           the data is storage in a .txt file"""

        cmd = "INIT:CONT OFF;:TRACE:DATA? 1"
        try:
            y_axis = (self.send_command(cmd, msgbx, True))
            if y_axis == None:
                raise TypeError("No se han recibido datos")
        except TypeError as e:
            msgbx.showerror(title="Sin respuesta", 
                message=f"Error! No se ha podido realizar el ploteo de los datos. {e}"
            )
        else:
            frecuencia_inicial = self.lband - ((self.symbol * 5) / 2)
            frecuencia_final = self.lband + ((self.symbol * 5) / 2)
            paso_frecuencias = (frecuencia_final - frecuencia_inicial) / (515 - 1)
            x_axis = []
            espectro = frecuencia_inicial
            for item in range(515):
                x_axis.append(round(espectro, 2))
                espectro += paso_frecuencias
            data_dict = {"potencias": y_axis.split(","), "frecuencias": x_axis}
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), fr"plots\plot\{file_name}.json")
            with open(path, "w") as f:
                json.dump(data_dict, f)