# Sistema de Gestión de Clientes, Facturas y Transacciones

## Datos del Aprendiz

**Nombre:** Esteban Castrillón Rodríguez
**Ficha:** 3407186
**Programa de Formación:** Tecnólogo en Análisis y Desarrollo de Software (ADSO)
**SENA**

---

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de una API REST utilizando FastAPI para la gestión de clientes, facturas y transacciones.

La aplicación permite realizar operaciones CRUD (Crear, Consultar, Actualizar y Eliminar) sobre las diferentes entidades del sistema, simulando una base de datos mediante listas en memoria.

---

## Tecnologías Utilizadas

* Python 3
* FastAPI
* Pydantic
* Uvicorn

---

## Actividades Realizadas

### 1. Creación de modelos con Pydantic

Se crearon los modelos necesarios para representar la información del sistema:

* Cliente
* Factura
* Transacción

Además, se definieron modelos específicos para:

* Crear registros
* Editar registros
* Mostrar información completa

---

### 2. Implementación del CRUD de Clientes

Se desarrollaron los siguientes endpoints:

#### Consultar todos los clientes

GET /clientes

#### Consultar cliente por ID

GET /clientes/{id}

#### Crear cliente

POST /clientes

#### Actualizar cliente

PUT /clientes/{id}

#### Eliminar cliente

DELETE /clientes/{id}

---

### 3. Implementación del CRUD de Facturas

Se desarrollaron los siguientes endpoints:

#### Consultar todas las facturas

GET /facturas

#### Crear factura asociada a un cliente

POST /facturas/{cliente_id}

#### Actualizar factura

PUT /facturas/{id}

#### Eliminar factura

DELETE /facturas/{id}

Además, se realizó la validación para verificar que el cliente exista antes de crear una factura.

---

### 4. Implementación del CRUD de Transacciones

Se desarrollaron los siguientes endpoints:

#### Consultar todas las transacciones

GET /transacciones

#### Consultar transacción por ID

GET /transacciones/{id}

#### Crear transacción

POST /transacciones/{factura_id}

#### Actualizar transacción

PUT /transacciones/{id}

#### Eliminar transacción

DELETE /transacciones/{id}

También se realizaron validaciones para verificar la existencia del cliente y de la factura antes de registrar una transacción.

---

### 5. Cálculo automático del valor total de la factura

Se implementó una propiedad calculada que permite obtener automáticamente el valor total de una factura a partir de las transacciones registradas.

Fórmula utilizada:

Valor Total = Cantidad × Valor Unitario

La suma de todas las transacciones corresponde al total de la factura.

---

### 6. Manejo de errores

Se implementaron validaciones para:

* Clientes inexistentes.
* Facturas inexistentes.
* Transacciones inexistentes.
* Asociaciones incorrectas entre clientes y facturas.

---

### 7. Pruebas de funcionamiento

Se realizaron pruebas utilizando la documentación automática de FastAPI:

/docs

Verificando:

* Creación de registros.
* Consulta de información.
* Actualización de datos.
* Eliminación de registros.
* Validaciones de errores.

---

## Ejecución del Proyecto

### Instalar dependencias

pip install fastapi uvicorn

### Ejecutar el servidor

uvicorn main:app --reload

### Acceder a la documentación

http://127.0.0.1:8000/docs

---

## Conclusión

Durante el desarrollo de esta actividad se aplicaron conceptos relacionados con APIs REST, FastAPI, validación de datos con Pydantic y operaciones CRUD. Además, se fortalecieron habilidades en la organización del código, manejo de rutas y validación de información dentro de una aplicación backend.
