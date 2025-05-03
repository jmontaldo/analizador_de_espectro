# Analizador de espectro

## Descripción
Este proyecto trata sobre la creación de un controlador para el analizador de espectro **ANRITSU MS27101A**, mediante el cuál se puedan automatizar las tareas de carga de la información para centrar las portadoras satelitales a través de un archivo csv y realizar los ploteos de las mismas para su posterior analisis.

*- Las señales que se encuentran actualmente en el archivo son a modo de ejemplo -*

## Uso
Una vez que se ejecuta el programa, primero buscamos una señal mediante el nombre, en la barra de búsqueda. La señal buscada
aparecera dentro del treeview, seleccionamos la señal y cargamos la información. Si deseamos realizar un ploteo de la portadora
en el analizador, bastará con seleccionar la opción y asignarle un nombre al archivo. El archivo generado será del tipo json,
para graficarlo, debemos seleccionar el menú 'archivo --> abrir' y seleccionar el archivo deseado.

### Imagenes

![programa_ejecutandose_con_analizador_de_espectro](/main/imgs/analizer_encuentro.jpg)

![ploteo_de_portadora](/main/imgs/EncuentroCarrier.webp)

![programa_con_analizador](/main/imgs/analizer_hbo.jpg)

![ploteo_de_portadora_2](/main/imgs/HBO2PanCarrier.webp)

## Autor
**jmontaldo**