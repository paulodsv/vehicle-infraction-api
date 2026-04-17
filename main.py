from fastapi import FastAPI
from app.routers.auth import auth_router
from app.routers.vehicle import vehicle_router
from app.api.exception_handlers import register_exception_handlers


app = FastAPI(title="Vehicle Infractions Service", description="""
              API para gerenciamento e monitoramento de infrações de trânsito em frotas de transporte.

              Permite o cadastro e gerenciamento de veículos, autenticação de usuários e consulta
              de infrações individuais ou consolidadas por frota.

              Projetada para atender transportadoras que necessitam de maior controle sobre multas,
              facilitando a análise, organização e acompanhamento das infrações de seus veículos.

              Conta com integração a sistemas externos para obtenção de dados atualizados de infrações.
              """,
              contact={
                  "name": "Paulo Henrique",
                  "email": "paulovieiradias064@gmail.com"
              },
              docs_url="/docs",
              redoc_url="/redoc",
              version="1.0.0")

register_exception_handlers(app)
app.include_router(auth_router)
app.include_router(vehicle_router)


