from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import Optional

from fastapi import FastAPI

app = FastAPI(
    title="Remuneraciones API (Ejemplo con datos ficticios de McDonald's)",
    description="API para obtener datos de remuneraciones",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Remuneraciones",
            "description": "API para obtener datos de remuneraciones"
        }
    ],
)

# Configuración de CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a la base de datos
conn = sqlite3.connect('remuneraciones.db')

# Definición de modelos para los datos
class Trabajador(BaseModel):
    id: int
    nombre_completo: str
    rut: str
    fecha_nacimiento: str
    genero: str
    estado_civil: str
    nacionalidad: str
    direccion: str
    fecha_ingreso: str
    tipo_contrato: str
    fecha_termino_contrato: Optional[str] = None
    jornada_trabajo: str
    categoria_laboral: str
    cargo: str
    centro_costo: str
    afp: str

class Remuneracion(BaseModel):
    id: int
    trabajador_id: int
    sueldo_base: float
    gratificaciones: float
    bonos: float
    horas_extra: float
    aguinaldos: float
    asignaciones: float
    descuentos: float
    remuneracion_total_imponible: float
    remuneracion_liquida: float

# Endpoint para obtener todos los trabajadores
@app.get("/trabajadores/")
async def get_trabajadores():
    conn = sqlite3.connect('remuneraciones.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trabajadores")
    rows = cursor.fetchall()
    trabajadores = []
    for row in rows:
        trabajador = Trabajador(
            id=row[0],
            nombre_completo=row[1],
            rut=row[2],
            fecha_nacimiento=row[3],
            genero=row[4],
            estado_civil=row[5],
            nacionalidad=row[6],
            direccion=row[7],
            fecha_ingreso=row[8],
            tipo_contrato=row[9],
            fecha_termino_contrato=row[10],
            jornada_trabajo=row[11],
            categoria_laboral=row[12],
            cargo=row[13],
            centro_costo=row[14],
            afp=row[15]
        )
        trabajadores.append(trabajador)
        conn.close()
    return trabajadores

# Endpoint para obtener todas las remuneraciones
@app.get("/remuneraciones/")
async def get_remuneraciones():
    conn = sqlite3.connect('remuneraciones.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM remuneraciones")
    rows = cursor.fetchall()
    remuneraciones = []
    for row in rows:
        remuneracion = Remuneracion(
            id=row[0],
            trabajador_id=row[1],
            sueldo_base=row[2],
            gratificaciones=row[3],
            bonos=row[4],
            horas_extra=row[5],
            aguinaldos=row[6],
            asignaciones=row[7],
            descuentos=row[8],
            remuneracion_total_imponible=row[9],
            remuneracion_liquida=row[10]
        )
        remuneraciones.append(remuneracion)
        conn.close()
    return remuneraciones

# Endpoint para obtener un trabajador por ID
@app.get("/trabajadores/{trabajador_id}")
async def get_trabajador(trabajador_id: int):
    conn = sqlite3.connect('remuneraciones.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trabajadores WHERE id = ?", (trabajador_id,))
    row = cursor.fetchone()
    if row:
        trabajador = Trabajador(
            id=row[0],
            nombre_completo=row[1],
            rut=row[2],
            fecha_nacimiento=row[3],
            genero=row[4],
            estado_civil=row[5],
            nacionalidad=row[6],
            direccion=row[7],
            fecha_ingreso=row[8],
            tipo_contrato=row[9],
            fecha_termino_contrato=row[10],
            jornada_trabajo=row[11],
            categoria_laboral=row[12],
            cargo=row[13],
            centro_costo=row[14],
            afp=row[15]
        )
        conn.close()
        return trabajador
    else:
        return {"error": "Trabajador no encontrado"}
        
    
    

# Endpoint para obtener una remuneración por ID
@app.get("/remuneraciones/{remuneracion_id}")
async def get_remuneracion(remuneracion_id: int):
    conn = sqlite3.connect('remuneraciones.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM remuneraciones WHERE id = ?", (remuneracion_id,))
    row = cursor.fetchone()
    if row:
        remuneracion = Remuneracion(
            id=row[0],
            trabajador_id=row[1],
            sueldo_base=row[2],
            gratificaciones=row[3],
            bonos=row[4],
            horas_extra=row[5],
            aguinaldos=row[6],
            asignaciones=row[7],
            descuentos=row[8],
            remuneracion_total_imponible=row[9],
            remuneracion_liquida=row[10]
        )
        conn.close()
        return remuneracion
        
    else:
        return {"error": "Remuneración no encontrada"}
    
@app.get("/trabajadores/{trabajador_id}/indicadores_laborales")
def get_indicadores_laborales(trabajador_id: int):
    conn = sqlite3.connect('remuneraciones.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM indicadores_laborales WHERE trabajador_id = ?", (trabajador_id,))
    indicadores = cursor.fetchall()
    conn.close()
    return [{"costo_laboral": row[2], "evolucion_salarial": row[3], "rotacion_personal": row[4], "promedio_ausencias": row[5]} for row in indicadores]

@app.get("/trabajadores/{trabajador_id}/cotizaciones")
def get_cotizaciones(trabajador_id: int):
    conn = sqlite3.connect('remuneraciones.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cotizaciones WHERE trabajador_id = ?", (trabajador_id,))
    cotizaciones = cursor.fetchall()
    conn.close()
    return [{"afp": row[1], "porcentaje_cotizacion": row[2], "seguro_cesantia": row[3], "sistema_salud": row[4], "cotizacion_salud": row[5], "seguro_invalidez": row[6], "aporte_empleador_accidentes": row[7]} for row in cotizaciones]

@app.get("/trabajadores/{trabajador_id}/asistencias_horas_extras")
def get_asistencias_horas_extras(trabajador_id: int):
    conn = sqlite3.connect('remuneraciones.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM asistencias_horas_extras WHERE trabajador_id = ?", (trabajador_id,))
    asistencias = cursor.fetchall()
    conn.close()
    return [{"horario_trabajo": row[1], "dias_trabajados": row[2], "permisos_legales": row[3], "vacaciones": row[4], "licencias_medicas": row[5], "inasistencias": row[6], "horas_extras": row[7]} for row in asistencias]


# Inicialización del servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)