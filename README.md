# Lenguaje de Programación Mercu

Se ha creado un Podscast con la tecnología de "https://notebooklm.google.com/" **MercuPodcast.mp4** que explica el contenido de este repositorio

Mercu es un lenguaje de programación interpretado y personalizado, diseñado como prueba de concepto en la creación de un lenguaje de programación. Este documento proporciona una guía completa sobre cómo utilizar Mercu, incluyendo explicaciones detalladas y ejemplos prácticos.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso Básico](#uso-básico)
- [Sintaxis y Características](#sintaxis-y-características)
  - [Variables y Tipos de Datos](#variables-y-tipos-de-datos)
  - [Operadores](#operadores)
  - [Estructuras Condicionales](#estructuras-condicionales)
  - [Funciones Nativas](#funciones-nativas)
- [Ejemplos](#ejemplos)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Instalación

Para ejecutar programas escritos en Mercu, necesitas clonar este repositorio y tener Python 3.10 o superior instalado en tu sistema.

    git clone https://github.com/pentarix1996/mercu-lang.git
    cd mercu-lang
    pip install -r requirements.txt

## Uso Básico

Para ejecutar un archivo escrito en Mercu, utiliza el comando:

    ./mercu ./tu_archivo.mer

Asegúrate de que el archivo `mercu.py` tenga permisos de ejecución y que esté en tu variable de entorno `PATH` si deseas ejecutarlo desde cualquier lugar.

## Sintaxis y Características

### Variables y Tipos de Datos

Mercu soporta los siguientes tipos de datos:

- **Números enteros**: Valores numéricos sin decimales, por ejemplo, `int`.
- **Cadenas de texto**: Texto encerrado entre comillas dobles o simples, por ejemplo, `"Hola, mundo"`.
- **Booleanos**: Valores lógicos `True` o `False`.
- **Diccionarios**: Colecciones de pares clave-valor, por ejemplo, `{ "clave": "valor" }`.

**Ejemplo:**

    number = 42
    my_str = "Hola, Mercu!"
    is_true = True
    my_dict = { "nombre": "Mercu", "version": 1.0 }

**Explicación:**

- `number` es una variable entera que almacena el valor `42`.
- `my_str` es una cadena de texto que contiene `"Hola, Mercu!"`.
- `is_true` es una variable booleana con el valor `True`.
- `my_dict` es un diccionario con clave/valor. Se puede utilizar como clave cualquier tipo de dato hashable (Salvo variables asignadas) `"nombre"` y `"version"`.

### Operadores

Mercu soporta los siguientes operadores para realizar operaciones:

#### Operadores Aritméticos

- `+` (Suma): Añade dos valores.
- `-` (Resta): Resta un valor de otro.
- `*` (Multiplicación): Multiplica dos valores.
- `/` (División): Divide un valor por otro.

**Ejemplo:**

    a = 10
    b = 5
    suma = a + b       # Resultado: 15
    resta = a - b      # Resultado: 5
    producto = a * b   # Resultado: 50
    division = a / b   # Resultado: 2.0

#### Operadores Lógicos

- `AND`: Devuelve `True` si ambos operandos son `True`.
- `OR`: Devuelve `True` si al menos uno de los operandos es `True`.
- `NOT`: Invierte el valor lógico del operando.

**Ejemplo:**

    verdadero = True
    falso = False

    resultado_and = verdadero AND falso   # Resultado: False
    resultado_or = verdadero OR falso     # Resultado: True
    resultado_not = NOT verdadero         # Resultado: False

#### Operadores Relacionales

- `==` (Igual a): Comprueba si dos valores son iguales.
- `!=` (Diferente de): Comprueba si dos valores son diferentes.
- `<` (Menor que): Comprueba si un valor es menor que otro.
- `>` (Mayor que): Comprueba si un valor es mayor que otro.
- `<=` (Menor o igual que): Comprueba si un valor es menor o igual que otro.
- `>=` (Mayor o igual que): Comprueba si un valor es mayor o igual que otro.

**Ejemplo:**

    x = 10
    y = 20

    es_igual = x == y          # Resultado: False
    es_menor = x < y           # Resultado: True
    es_mayor_o_igual = x >= y  # Resultado: False

### Estructuras Condicionales

Las estructuras condicionales permiten ejecutar código basándose en condiciones.

#### Sintaxis:

    if condicion:
    {
        # Código a ejecutar si la condición es verdadera
    }
    elif otra_condicion:
    {
        # Código a ejecutar si la otra condición es verdadera
    }
    else:
    {
        # Código a ejecutar si ninguna condición anterior es verdadera
    }

**Nota:** Los bloques de código dentro de las estructuras condicionales se encierran entre llaves `{ }`.

#### Ejemplo:

    edad = 25

    if edad >= 18:
    {
        print("Eres mayor de edad.")
    }
    else:
    {
        print("Eres menor de edad.")
    }

### Funciones Nativas

Mercu incluye alguinas funciones incorporadas de forma nativa.

#### `print()`

Imprime valores en la consola.

**Sintaxis:**

    print(valor1, valor2, ...)

**Ejemplo:**

    name = "Mercu!"
    print("Hola ", name)

**Salida Esperada:**

    Hola, Mercu!

#### `connect_db()`

Conecta a una base de datos SQLite.

**Sintaxis:**

    connect_db(ruta_de_la_base_de_datos)

**Ejemplo:**

    connect_db("mi_base_de_datos.db")

**Explicación:**

- Establece una conexión con la base de datos SQLite ubicada en `"mi_base_de_datos.db"`.

#### `db_insert()`

Inserta información en una tabla dada, si no existe la crea.

**Sintaxis:**

    db_insert(table_name: str, data: dict[Any, Any])

**Ejemplo:**

    data = {"name": "Antonio", age: 28}
    db_insert("users", data)

#### `db_query()`

Imprime por pantalla toda la información almacenada en la tabla solicitada.

**Sintaxis:**

    db_query(table_name: str)

**Ejemplo:**

    db_query("users")

#### `create_api()`

Crea y levanta una API utilizando FastAPI.

**Sintaxis:**

    create_api(titulo_de_la_api: str)

**Ejemplo:**

    create_api("API de Ejemplo")

**Explicación:**

- Crea y ejecuta una API con el título `"API de Ejemplo"` en el puerto `8000`.

## Ejemplos

A continuación, se presentan ejemplos prácticos ubicados en el directorio `examples`. Cada ejemplo incluye su explicación y el resultado esperado.

### Ejemplo 1: Operaciones Básicas

**Archivo:** `examples/operaciones_basicas.mer`

    a = 10
    b = 5
    suma = a + b
    resta = a - b
    multiplicacion = a * b
    division = a / b

    print("Suma:", suma)
    print("Resta:", resta)
    print("Multiplicación:", multiplicacion)
    print("División:", division)

**Salida Esperada:**

    Suma:15
    Resta:5
    Multiplicación:50
    División:2.0

### Ejemplo 2: Uso de Operadores Lógicos

**Archivo:** `examples/logic_operators.mer`

    active = True
    inactive = False

    print("Variable 'active': ", active)
    print("Variable 'inactive': ", inactive)

    result = active AND inactive
    print("True AND False = ", result)

    result = active AND inactive
    print("True AND True = ", result)

    result = active OR inactive
    print("True OR False = ", result)

    result = NOT active
    print("NOT active = ", result)

    result = NOT inactive
    print("NOT inactive = ", result)

**Salida Esperada:**

    Variable 'active': True
    Variable 'inactive': False
    True AND False = False
    True AND True = False
    True OR False = True
    NOT active = False
    NOT inactive = True

### Ejemplo 3: Estructuras Condicionales

**Archivo:** `examples/if_else_example.mer`

    temperature = 30

    if temperature > 25:
    {
        print("Hace calor.")
    }
    elif temperature < 15:
    {
        print("Hace frío.")
    }
    else:
    {
        print("El clima es templado.")
    }

**Salida Esperada:**

    Hace calor.

### Ejemplo 4: Uso de Diccionarios

**Archivo:** `examples/dict_example.mer`

    usuario = { "nombre": "Ana", "edad": 28 }

    print("Nombre del usuario:", usuario["nombre"])
    print("Edad del usuario:", usuario["edad"])

**Salida Esperada:**

    Nombre del usuario: Ana
    Edad del usuario: 28

### Ejemplo 5: Conexión a Base de Datos y Creación de API

**Archivo:** `examples/db_example.mer | examples/api_example.mer`

- Conecta a una base de datos SQLite, introduce datos de usuarios y los muestra por pantalla. Por otro lado, levanta una API utilizando FastAPI.

## Contribución

Si deseas contribuir al desarrollo de Mercu, sigue estos pasos:

1. Realiza un fork del repositorio:

       git clone https://github.com/pentarix1996/mercu_language.git

2. Crea una nueva rama para tu funcionalidad:

       git checkout -b mi-nueva-funcionalidad

3. Realiza tus cambios y haz commits descriptivos:

       git commit -am "Agrego nueva característica X"

4. Envía tus cambios a tu repositorio/fork:

       git push origin mi-nueva-funcionalidad

5. Abre un Pull Request en GitHub.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
