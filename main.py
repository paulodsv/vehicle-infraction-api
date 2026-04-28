from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from app.api.exception_handlers import register_exception_handlers
from app.core.logging_config import setup_logging
from app.routers.auth import auth_router
from app.routers.health import health_router
from app.routers.infraction import infractions_router
from app.routers.senatran import senatran_router
from app.routers.user import user_router
from app.routers.vehicle import vehicle_router

setup_logging()

app = FastAPI(title="Vehicle Infractions Service", description="""
API para gerenciamento e monitoramento de infrações de trânsito em frotas de transporte.
Permite o cadastro e gerenciamento de veículos, autenticação de usuários e consulta de infrações individuais ou consolidadas por frota.
Projetada para atender transportadoras que necessitam de maior controle sobre multas, facilitando a análise, organização e acompanhamento das infrações de seus veículos.
Conta com integração a sistemas externos para obtenção de dados atualizados de infrações.
""",
              contact={
                  "name": "Paulo Henrique",
                  "email": "paulovieiradias064@gmail.com"
              },
              docs_url=None,
              version="1.0.0")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Vehicle Infractions Service",
        swagger_css_url="/static/swagger-custom.css"
    )

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(vehicle_router)
app.include_router(infractions_router)
app.include_router(senatran_router)
app.include_router(user_router)


