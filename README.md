# updateGoogleDNS
Actualiza la IP de Google DNS para que siempre esté actualizada en un servidor GNU/Linux de IP dinámica.

Se sugiere que la carpeta esté dentro de “/opt”, sin embargo puede modificar esta ruta en el archivo "updateGoogleDNS" en la siguiente variable:

```Shell
#!/bin/bash

PATH_INSTALL_SCRIPT_PYTHON="/opt/updateGoogleDNS"
```
Puede que requiera permisos especiales para crear la carpeta de logs en "/var/log"

Para instalar las dependencias del script de python requiere tener instalado python3 y pip3, si satisface estas dependencias podrá usar el siguiente comando:

```Shell
pip install -r requirements.txt
```
Habrá que agregar una línea al "crontab", se sugiere que sea cada 5 minutos pero puede ajustar este tiempo a su conveniencia, así como colocar el usuario que desea que ejecute este proceso, se recomienda que no sea "root":

```Shell
*/5 * * * *     <USER>   /opt/updateGoogleDNS/updateGoogleDNS
```
---

Update the Google DNS IP so it is always updated on a dynamic GNU/Linux IP server.

It is suggested that the folder be within “/opt”, however you can modify this path in the "updateGoogleDNS" file in the following variable:

```Shell
#!/bin/bash

PATH_INSTALL_SCRIPT_PYTHON="/opt/updateGoogleDNS"
```

You may require special permissions to create the log folder in "/var/log"

To install the python script dependencies you need to have python3 and pip3 installed, if you satisfy these dependencies you can use the following command:

```Shell
pip install -r requirements.txt
```
It will be necessary to add a line to the "crontab", it is suggested that it be every 5 minutes but you can adjust this time to your convenience, as well as placing the user that you want to execute this process, it is recommended that it is not "root":

```Shell
*/5 * * * *     <USER>   /opt/updateGoogleDNS/updateGoogleDNS
```