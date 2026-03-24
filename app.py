from flask import Flask, render_template, request
from datetime import datetime, dategit 

app = Flask(__name__)



def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad

def signo(dia, mes):

    if (mes==3 and dia>=21) or (mes==4 and dia<=19):
        return "Aries"
    elif (mes==4 and dia>=20) or (mes==5 and dia<=20):
        return "Tauro"
    elif (mes==5 and dia>=21) or (mes==6 and dia<=20):
        return "Géminis"
    elif (mes==6 and dia>=21) or (mes==7 and dia<=22):
        return "Cáncer"
    elif (mes==7 and dia>=23) or (mes==8 and dia<=22):
        return "Leo"
    elif (mes==8 and dia>=23) or (mes==9 and dia<=22):
        return "Virgo"
    elif (mes==9 and dia>=23) or (mes==10 and dia<=22):
        return "Libra"
    elif (mes==10 and dia>=23) or (mes==11 and dia<=21):
        return "Escorpio"
    elif (mes==11 and dia>=22) or (mes==12 and dia<=21):
        return "Sagitario"
    elif (mes==12 and dia>=22) or (mes==1 and dia<=19):
        return "Capricornio"
    elif (mes==1 and dia>=20) or (mes==2 and dia<=18):
        return "Acuario"
    else:
        return "Piscis"

@app.route("/", methods=["GET","POST"])
def index():

    resultado=""
    mensaje_imc=""
    porcentaje=0
    color="green"
    edad=""
    signo_zodiacal=""
    mensaje_pais=""
    fecha_actual=datetime.now().strftime("%d/%m/%Y")

    if request.method=="POST":

        nombre=request.form["nombre"]
        fecha=request.form["fecha"]

        fecha_nacimiento=datetime.strptime(fecha,"%d/%m/%Y")

        pais=request.form["pais"].lower()

        peso=float(request.form["peso"])
        altura=float(request.form["altura"])

        if altura <= 0:
            resultado="Altura inválida"
            return render_template("index.html", resultado=resultado)

        edad=calcular_edad(fecha_nacimiento)
        signo_zodiacal=signo(fecha_nacimiento.day,fecha_nacimiento.month)

        if pais in ["peru","perú"]:
            mensaje_pais="¡Tierra de Machu Picchu!"
        elif pais in ["mexico","méxico"]:
            mensaje_pais="¡Cuna del mariachi!"
        elif pais=="argentina":
            mensaje_pais="¡Tierra del tango!"
        else:
            mensaje_pais="¡Un país increíble!"

        imc=round(peso/(altura**2),2)

        if imc < 18.5:

            estado="Bajo peso"
            color="orange"

            peso_minimo=round(18.5*(altura**2),1)
            diferencia=round(peso_minimo-peso,1)

            mensaje_imc=f"Tienes bajo peso. Deberías subir aproximadamente {diferencia} kg para alcanzar el peso saludable."

        elif imc < 25:

            estado="Peso saludable"
            color="green"

            mensaje_imc="¡Estás en un peso saludable! Mantente así 💪"

        elif imc < 30:

            estado="Sobrepeso"
            color="gold"

            peso_maximo=round(24.9*(altura**2),1)
            diferencia=round(peso-peso_maximo,1)

            mensaje_imc=f"Tienes sobrepeso. Deberías perder aproximadamente {diferencia} kg para alcanzar el límite saludable."

        else:

            estado="Obesidad"
            color="red"

            peso_maximo=round(24.9*(altura**2),1)
            diferencia=round(peso-peso_maximo,1)

            mensaje_imc=f"Tienes obesidad. Deberías perder aproximadamente {diferencia} kg para alcanzar un peso saludable."

        porcentaje=min(int(imc*4),100)

        resultado=f"{nombre}, tu IMC es {imc} ({estado})"

    return render_template("index.html",
                           resultado=resultado,
                           mensaje_imc=mensaje_imc,
                           fecha=fecha_actual,
                           porcentaje=porcentaje,
                           color=color,
                           edad=edad,
                           signo=signo_zodiacal,
                           mensaje_pais=mensaje_pais)

if __name__=="__main__":
      app.run(host="0.0.0.0", port=10000)