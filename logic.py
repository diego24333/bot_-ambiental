import random
     
def preguntas():
    pregunta = random.randint(0, 3)
    if pregunta== 0:
        return "¿Cierras la llave cuando te lavas los dientes?"
    elif pregunta==1:
        return "¿Separas  el plastico de la demas basura?"
    elif pregunta==2:
        return "¿duras mucho tiempo en la ducha?" 
    elif pregunta==3:
        return "¿usas desodorante en aerosol?"

   