from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from utils import get_generate_smiles, get_predict, prediction_to_table

templates = Jinja2Templates('./templates/molgan')

async def root_view(request):
    return templates.TemplateResponse('index.html', {'request': request})

async def models_view(request):
    return templates.TemplateResponse('models.html', {'request': request})

async def jtvae_view(request):
    smiles = await get_generate_smiles()
    return templates.TemplateResponse('jtvae.html', {'request': request, 'smiles': smiles})

async def mpnn_view(request, smiles=''):
    return templates.TemplateResponse('mpnn.html', {'request': request, 'smiles': smiles})

async def mpnn_predict_view(request, smiles=''):
    prediction = await get_predict(smiles)
    if prediction['status'] == 'NOT OK':
        return templates.TemplateResponse('mpnn_prediction.html', {'request': request, 'prediction_table': None, 'smiles': smiles})
    prediction_table = await prediction_to_table(prediction)
    return templates.TemplateResponse('mpnn_prediction.html', {'request': request, 'prediction_table': prediction_table, 'smiles': smiles})

async def mpnn_list_view(request, filename):
    return templates.TemplateResponse('mpnn_list.html', {'request': request, 'filename': filename})

async def mpnn_list_predict_view(request, filename):
    return templates.TemplateResponse('mpnn_list_predict.html', {'request': request, 'filename': filename})

async def get_generate_smiles_for_mpnn():
    smiles = await get_generate_smiles()
    return smiles