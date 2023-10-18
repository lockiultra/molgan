from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from utils import get_generate_smiles, get_predict_list
from views import *

app = FastAPI()
app.mount('/static', StaticFiles(directory='./static'), name='static')
app.mount('/tmp', StaticFiles(directory='./tmp'), name='tmp')

@app.get('/')
async def index(request: Request):
    return await root_view(request)

@app.get('/models')
async def models(request: Request):
    return await models_view(request)

@app.get('/models/jtvae')
async def jtvae(request: Request):
    return await jtvae_view(request)

@app.get('/models/mpnn')
async def mpnn(request: Request):
    smiles=request.query_params.get('smiles', '')
    return await mpnn_view(request, smiles)

@app.post('/models/mpnn')
async def mpnn(request: Request, smiles = Form()):
    return await mpnn_predict_view(request, smiles)
    
@app.get('/models/mpnn_list')
async def mpnn_list(request: Request):
    filename = request.query_params.get('filename', '')
    return await mpnn_list_view(request, filename)

@app.post('/models/mpnn_list')
async def mpnn_list(request: Request, smiles_file = Form()):
    smiles_list = await smiles_file.read()
    predict_filename = await get_predict_list(smiles_list)
    return RedirectResponse('/models/mpnn_list/predict?filename='+predict_filename)

@app.post('/models/mpnn_list/predict')
async def mpnn_list_predict(request: Request):
    filename = request.query_params.get('filename', '')
    filename = '/tmp/' + filename.split('/')[-1]
    return await mpnn_list_predict_view(request, filename)

@app.get('/get_generate_smiles_for_mpnn')
async def get_generate_smiles_for_mpnn(request: Request):
    smiles = await get_generate_smiles()
    return RedirectResponse('/models/mpnn?smiles='+smiles)

# Middleware

@app.middleware('http')
async def catch_exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        assert response.status_code != 404
        return response
    except Exception as e:
        print(e)
        return templates.TemplateResponse('404.html', {'request': request, 'error': str(e)})