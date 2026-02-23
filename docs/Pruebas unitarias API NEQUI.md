# **Pruebas unitarias**

Pruebas con palabras filtradas: 

Json Ejemplo: {

"message\_id": "msg-7",
"session\_id": "session-abcdef",
"content": "Hola, Prueba con palabritas **spam** u **ofensivo** para este contenido",
"timestamp": "2023-06-15T14:30:00Z",
"sender": "system"

}

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.001.png)


Respuesta: 

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.002.png)

Se guarda en la base de datos: y realiza la “censura” de las palabras “prohibidas” y deja el registro de metadatos, en este caso conteo de palabras = 10.

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.003.png)



Se realiza, la validación en el swagger y se envían datos sin la KEY: 

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.004.png)

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.005.png)

Pruebas usando correctamente la KEY: 

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.006.png)

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.007.png)

El mensaje se guarda correctamente en el archivo de persistencia .db el cual se abre en el gestor de bases de daatos SQLITE: 

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.008.png)

Pruebas con WebSocket + Swagger: 

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.009.png)

El postman se observa que llega el evento: 

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.010.png)

Se agrega un archivo HTML para ver el evento:

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.011.png)

Llegando a postman: 

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.012.png)

Monitor desde el navegador: 

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.013.png)

Pruebas Automatizadas Pytest: 

![](assets/Aspose.Words.481a6776-252b-466e-8010-4cfcd8ded452.014.png)

`		`Elaborado por Cristian Olvany Loaiza Durán
