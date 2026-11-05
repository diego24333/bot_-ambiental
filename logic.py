import random

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>"
    password = ""

    for i in range(pass_length):
        password += random.choice(elements)

    return password


def gen_emodji():
    emodji = ["\U0001f600", "\U0001f642", "\U0001F606", "\U0001F923"]
    return random.choice(emodji)


def flip_coin():
    flip = random.randint(0, 1)
    if flip == 0:
        return "HEADS"
    else:
        return "TAILS"


PUNTOS_POR_ACIERTO = 2
PUNTOS_POR_ERROR = 1

SI = ["si", "sí", "s"]
NO = ["no", "n"]

PREGUNTAS = [
    {
        "pregunta": "¿Cierras la llave cuando te lavas los dientes?",
        "respuestas": SI, "sino": True,
        "tip": "Cerrar la llave mientras te cepillas ahorra muchos litros de agua cada día.",
    },
    {
        "pregunta": "¿Separas el plástico de la demás basura?",
        "respuestas": SI, "sino": True,
        "tip": "Separar el plástico permite que se pueda reciclar en vez de terminar en un basurero.",
    },
    {
        "pregunta": "¿Duras mucho tiempo en la ducha?",
        "respuestas": NO, "sino": True,
        "tip": "Duchas más cortas ahorran agua y también la energía que se usa para calentarla.",
    },
    {
        "pregunta": "¿Usas desodorante en aerosol?",
        "respuestas": NO, "sino": True,
        "tip": "Los aerosoles usan gases que contaminan el aire y sus envases son difíciles de reciclar. "
               "Las opciones en barra o roll-on son mejores.",
    },
    {
        "pregunta": "¿Apagas las luces cuando sales de una habitación?",
        "respuestas": SI, "sino": True,
        "tip": "Apagar las luces que no usas reduce el consumo de electricidad.",
    },
    {
        "pregunta": "¿Llevas tu propia bolsa reutilizable cuando vas de compras?",
        "respuestas": SI, "sino": True,
        "tip": "Una bolsa reutilizable evita decenas de bolsas plásticas de un solo uso al año.",
    },
    {
        "pregunta": "¿Dejas el cargador enchufado todo el día sin usarlo?",
        "respuestas": NO, "sino": True,
        "tip": "Un cargador enchufado sigue consumiendo un poco de energía aunque no cargue nada.",
    },
    {
        "pregunta": "¿Usas botellas de plástico de un solo uso todos los días?",
        "respuestas": NO, "sino": True,
        "tip": "Una botella reutilizable reduce muchísimo los residuos plásticos.",
    },
    {
        "pregunta": "Adivinanza: ¿Qué tiene agujas, pero no cose?",
        "respuestas": ["reloj", "un reloj"], "sino": False,
        "tip": "",
    },
]

TIENDA = {
    "escudo": {
        "nombre": "Escudo",
        "precio": 5,
        "desc": "La próxima respuesta incorrecta no te quita puntos.",
    },
    "doble": {
        "nombre": "Doble puntos",
        "precio": 8,
        "desc": "Duplica los puntos de tus próximas 3 respuestas correctas.",
    },
}

usuarios = {}


def get_usuario(uid):
    if uid not in usuarios:
        usuarios[uid] = [0, 0, 0]
    return tuple(usuarios[uid])


def guardar(uid, puntos, escudos, dobles):
    usuarios[uid] = [puntos, escudos, dobles]


def ranking_top(limite=10):
    ordenados = sorted(usuarios.items(), key=lambda x: x[1][0], reverse=True)
    return [(uid, datos[0]) for uid, datos in ordenados[:limite]]


def preguntas():
    return random.choice(PREGUNTAS)


def normalizar(texto):
    return texto.strip().lower()


def respuesta_valida(pregunta, texto):
    if pregunta.get("sino"):
        return normalizar(texto) in SI + NO
    return True


def procesar_respuesta(uid, pregunta, respuesta):
    puntos, escudos, dobles = get_usuario(uid)
    correctas = [normalizar(r) for r in pregunta["respuestas"]]

    if normalizar(respuesta) in correctas:
        ganados = PUNTOS_POR_ACIERTO
        extra = ""
        if dobles > 0:
            ganados *= 2
            dobles -= 1
            extra = f" (doble puntos, te quedan {dobles} usos)"
        puntos += ganados
        guardar(uid, puntos, escudos, dobles)
        saludo = "¡Muy bien, ese es un hábito ecológico!" if pregunta.get("sino") else "¡Correcto!"
        return f"{saludo} +{ganados} puntos{extra}. Total: **{puntos}**"

    if pregunta.get("sino"):
        detalle = f"Ese no es el hábito más ecológico.\nConsejo: {pregunta['tip']}"
    else:
        detalle = f"Incorrecto. La respuesta era **{pregunta['respuestas'][0]}**."

    if escudos > 0:
        escudos -= 1
        guardar(uid, puntos, escudos, dobles)
        return f"{detalle}\nTu escudo te protegió, no perdiste puntos. Total: **{puntos}**"

    perdidos = min(PUNTOS_POR_ERROR, puntos)
    puntos -= perdidos
    guardar(uid, puntos, escudos, dobles)
    return f"{detalle}\nPierdes {perdidos} punto(s). Total: **{puntos}**"


def comprar_item(uid, clave):
    producto = TIENDA[clave]
    puntos, escudos, dobles = get_usuario(uid)

    if puntos < producto["precio"]:
        return False, f"No te alcanza: tienes {puntos} y cuesta {producto['precio']}."

    puntos -= producto["precio"]
    if clave == "escudo":
        escudos += 1
    elif clave == "doble":
        dobles += 3

    guardar(uid, puntos, escudos, dobles)
    return True, f"Compraste {producto['nombre']}. Te quedan **{puntos}** puntos."
