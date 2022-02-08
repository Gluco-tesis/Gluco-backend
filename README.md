### Modificaciones a la BD

```SQL

ALTER TABLE glucometro.codes MODIFY COLUMN rest_code INT(5) DEFAULT NULL NULL;
ALTER TABLE glucometro.codes DROP COLUMN email;
ALTER TABLE glucometro.codes ADD user_id INT(11) NOT NULL;
ALTER TABLE glucometro.codes CHANGE user_id user_id INT(11) NOT NULL FIRST;
ALTER TABLE glucometro.codes CHANGE user_id user_id int(11) NOT NULL AFTER id;
ALTER TABLE glucometro.codes ADD CONSTRAINT codes_FK FOREIGN KEY (user_id) REFERENCES glucometro.usuarios(id);


```

# GLuco backend

Para que funcione el envio de mails es necesario configurar el archivo .env siguiendo lo escrito en el archivo .envExamples
Esta hecho para utilizar un mail gmail, y es necesario configurar la seguridad de gmail para que permitra el acceso.

1. ir gmail
2. tocar nuestra foto ir a "Gestionar tu cuenta de google"
3. ir a la barra lateral la opcion "Seguridad"
4. ir a la parte inferior y habilitar "Acceso de aplicaciones poco seguras"
5. Permitir el acceso de aplicaciones poco seguras: SÍ




