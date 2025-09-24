from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend.models import Base, Jugador
import requests
from bs4 import BeautifulSoup
from typing import Optional

#Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fantasy LaLiga API")

# Permitir CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://pabloesmo.github.io/FantasyTk",
    "https://pabloesmo.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # or ["*"] para permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

escudos = {
    "ATH": "https://assets.laliga.com/assets/2019/06/07/small/athletic.png",
    "ATL": "https://assets.laliga.com/assets/2019/06/07/small/atletico-de-madrid.png",
    "OSA": "https://assets.laliga.com/assets/2019/06/07/small/osasuna.png",
    "ALA": "https://assets.laliga.com/assets/2019/06/07/small/alaves.png",
    "ELC": "https://assets.laliga.com/assets/2019/06/07/small/elche.png",
    "BAR": "https://assets.laliga.com/assets/2019/06/07/small/barcelona.png",
    "GET": "https://assets.laliga.com/assets/2019/06/07/small/getafe.png",
    "GIR": "https://assets.laliga.com/assets/2019/06/07/small/girona.png",
    "LEV": "https://assets.laliga.com/assets/2019/06/07/small/levante.png",
    "RAY": "https://assets.laliga.com/assets/2019/06/07/small/rayo-vallecano.png",
    "CEL": "https://assets.laliga.com/assets/2019/06/07/small/celta.png",
    "ESP": "https://assets.laliga.com/assets/2019/06/07/small/espanyol.png",
    "MAH": "https://assets.laliga.com/assets/2019/06/07/small/mallorca.png",
    "BET": "https://assets.laliga.com/assets/2019/06/07/small/betis.png",
    "RMA": "https://assets.laliga.com/assets/2019/06/07/small/real-madrid.png",
    "OVI": "https://assets.laliga.com/assets/2019/06/07/small/oviedo.png",
    "RSG": "https://assets.laliga.com/assets/2019/06/07/small/real-sociedad.png",
    "SEV": "https://assets.laliga.com/assets/2019/06/07/small/sevilla.png",
    "CVC": "https://assets.laliga.com/assets/2019/06/07/small/valencia.png",
    "VIL": "https://assets.laliga.com/assets/2019/06/07/small/villarreal.png",
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/jugadores")
def buscar_jugadores(nombre: str = None, db: Session = Depends(get_db)):
    if nombre:
        return db.query(Jugador).filter(Jugador.nombre.ilike(f"%{nombre}%")).all()
    return db.query(Jugador).all()

# --- NUEVO ENDPOINT ---
@app.get("/jugador-imagen")
def obtener_imagen_jugador(nombre: str = Query(...), apellido: Optional[str] = None):
    """
    Devuelve la URL de la imagen de un jugador de FútbolFantasy
    """
    # TODO (a futuro): almaceno las imagenes de cada jugador en mi base de datos
    # TODO y así no tengo que hacer siempre una peticion HTTP. Más rapido, compruebo si 
    # TODO ya la tengo en mi base de datos y si no la tengo, SI hago la peticion HTTP.
    
    nombre_formateado = nombre.lower()
    if(apellido == ""):
        apellido_formateado = ""
    else:
        apellido_formateado = apellido.lower()
    url = f"https://www.futbolfantasy.com/jugadores/{nombre_formateado}-{apellido_formateado}"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        img_tag = soup.select_one("img.img.w-100.mb-1")

        if img_tag and img_tag.get("src"):
            image_url = img_tag["src"]
        else:
            # fallback si no hay imagen
            image_url = "https://media.futbolfantasy.com/thumb/400x400/v202209182308/uploads/images/jugadores/ficha/00.png"

        return {"image_url": image_url}

    except Exception as e:
        return {"image_url": "https://media.futbolfantasy.com/thumb/400x400/v202209182308/uploads/images/jugadores/ficha/00.png",
                "error": str(e)}

@app.get("/goleadores")
def obtener_goleadores():
    url = "https://www.laliga.com/leaderboard/todos-los-lideres?stat_competition=laliga-easports&stat=total_goals_ranking"
    goleadores = []

    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    for row in soup.select("tbody tr"):
        c = row.find_all("td")

        abreviado = c[3].get_text(strip=True)

        goleadores.append({
            "nombre": c[2].get_text(strip=True),
            "equipo": c[3].get_text(strip=True),
            "goles": c[5].get_text(strip=True),
            "escudo": escudos.get(abreviado,None) #pillo la URL de cada equipo
        })

    return goleadores

@app.get("/grafica-mercado-jugador")
def obtener_grafica_mercado(nombre: str = Query(...), apellido: Optional[str] = None):
    nombre_formateado = nombre.lower()
    if(apellido == ""):
        apellido_formateado = ""
    else:
        apellido_formateado = apellido.lower()
    url = f"https://www.futbolfantasy.com/jugadores/{nombre_formateado}-{apellido_formateado}"