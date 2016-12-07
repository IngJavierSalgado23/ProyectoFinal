#Informacion del proyecto final
Elaboracion de un task manager. Equipo: Antonio Javier Salgado Hernandez Clase: Sistemas Operativos

Librerias a importar
Plotly (sudo pip install plotly)
Tkinter (sudo apt-get gnome-disk-utility, sudo apt-get install python python-tk idle python-pmw python-imaging,sudo pip install tkintertable)
Matlib (sudo apt-get install python-matplotlib)
drawnow (sudo pip install drawnow)


Parcial 1 incluye las siguientes acciones:

1- Consigue los procesos corriendo y los sortea de tres formas: consumo de CPU, consumo de Memoria y PID (Dependiendo de la eleccion del usuario)

2- Matar Proceso. El usuario indica el pid del proceso a matar.

3-Mapea el disco. Indica cuantos archivos hay de cada extension en el disco (Idea brindada por el equipo de Raul, Allan y Jorge). Ademas indica la cantidad de memoria del disco duro, el espacio usado y el espacio disponible. Tambien el usuario tiene la opcion de ingresar un path para  recibir los archivos que existen en el path y su consumo de memoria. 

4- Guarda todas las acciones en un log, ubicado en /home/ingjaviersalgado23/crearLogs/LogProyectoFinal.txt.

5.Para cubrir la parte de crear proceso, hay un proceso extra que siempre esta obteniendo los procesos corriendo, los cual sera util en el momento de graficar performance.

6- La libreria que estoy planeando en utilizar es plotly. Requiere instalar la libreria plotly asi como crear una cuenta para entrar al servidor. Las graficas se realizaran en linea.

7- Cuanta con la grafica sobre el mapeo del disco usando plot.ly

2do Parcial Para correr el 2do parcial, solo se ocupa window.py y funciones.py correr window para iniciar el programa.
1- Tabla de procesos elaborando usando treeview y tk. Se refresca cada 5 segundos.
2- Se agregaron 3 botones para ordenar segun las columnas de consumo de cpu, consumo de memoria y PID
3- Para matar un proceso de la tabla, se debe primero seleccionarlo y aplicar click-derecho.
4- La grafica de distribucion del disco duro por archivos se logra usando plotly. Instalar y crear una cuenta de plotly para poder usarse. Despues de crear cuenta de plotly es necesario seguir las indicaciones descritas en el siguiente url https://plot.ly/python/getting-started/
5- La grafica de distribucion del disco duro por directorios no la he terminado, hasta el momento solo he conseguido saber quienes es el directorio padre su peso quienes son sus directorios hijos con su peso, sin embargo no he podido graficarla.
6- Grafica en tiempo real del consumo de memoria y cpu. Se logra oprimiendo su boton correspondiente en la gui. Cuando se presiona se crea un thread el cual consigue la informacion para graficarla. Se refresca cada segundo para simular el tiempo real. Para que se refrescara recibi ayuda de mi companero Carlos y utilize la libreria drawnow. La logica y la forma de conseguir la informacion en este metodo es mia, solo recibi ayuda en la parte de real time.

Tercer Parcial
1-Se obtuvieron 20gb addiciones de logs, los cuales juntadolos con el pasado suman un total de 30gb de logs.
2- Los 30 gbs de logs fueron analizados en el codigo y elaboro recomendaciones a partir de la lectura. Los analisis estan en la seccion de recommendaciones y estan visualizados en un trreview, donde indica la cantidad de cpu rpromedio, memoria usada en promedio, pid, user y las numeras de veces que estuvo activo mientras se elaboraban los logs.
3- Se anexo informacion de l a memoria virtual, swap y cache. Se anexo laposibilidad de graficar el uso de la memoria swap y el uso de la memoria fisica. Tambien se anexo un boton que te permite limpiar la memomoria cache y la memoria swap. Para poder correr la limpieza de memoria se debe de correr e archivo desde terminal con sudo.
4- Se nexaron los stats de la aplicacion en una pestana  adiccional con el nombre de informacion.
5. Se anexo el boton de mapeo por folders utilizando la libreria boabab.
