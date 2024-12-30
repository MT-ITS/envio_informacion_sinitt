<h1 align="center"> Componente Prototipo de Envio de Información al SINITT.</h1>

<h2> Descripción del Proyecto </h2>
Este codigo sirve para enviar información hacia el SINITT. Para esto el Ministerio de Transporte de Colombia creo un componente que crea una pagina web, mediante la cual las entidades o actores que van a utilizar el SINITT pueden enviar mensajes en DATEX_II 
mediante el protocolo statefull push.

La siguiente gráfica muestra las interrelaciones definidas para el uso del componente:


<h2>Instalación</h2>h2>
La entidad que desee utilizar este componente para comunicación con el SINITT deberá:

1. Descargar el código  
2. ubicarse en la carpeta raiz (donde esta el archivo requirements.txt) 
3. Instalar las librerias mediante el comando:

pip install -r requirements 

<h2>Utilización</h2>
La persona utilizando el código debe ir a la carpeta src y ejecutar lo siguiente:

python manage.py runserver

Esto abrira un servidor web corriendo en el computador local. Para acceder a este servicio el usuario debe entrar en un navegador y dar la siguiente URL:

http://127.0.0.1:8000/start/3

El numero que esta escrito en la url anterior puede tomar los siguiente valores de acuerdo al tipo de publicación que se desea entregar. La siguiente es la lista de valores validos

| Numero | tipo de publicación             |
| ------ | ------------------------------- |
| 1      | Measured Data Publication       |
| 2      | Elaborated Data Publication     |
| 3      | Situation Publication           |
| 4      | Measured Site Table Publication |
| 5      | Vms Publication                 |
| 6      | Vms Table Publication           |

La url dada (http://127.0.0.1:8000/start/3) sirve por tanto para enviar un mensaje de la publicación Situation Publication.
