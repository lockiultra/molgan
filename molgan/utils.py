import aiohttp
import settings
import json
from tempfile import NamedTemporaryFile
from models import Disease
from fastapi.responses import FileResponse

async def get_generate_smiles():
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.MOLGAN_API_SAMPLE_MOL) as response:
            smiles = await response.json()
            return smiles.get('SMILES')
        
async def get_predict(smiles):
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.MOLGAN_API_PREDICT+smiles) as response:
            return await response.json()
        
async def prediction_to_table(prediction):
    return [Disease(disease, pred) for disease, pred in zip(settings.DISEASES, prediction.values())]

async def get_predict_list(smiles_list):
    pred_list = []
    async with aiohttp.ClientSession() as session:
        for mol in smiles_list.splitlines():
            async with session.get(settings.MOLGAN_API_PREDICT+mol.decode()) as response:
                pred = await response.json()
                pred['smiles'] = mol.decode()
                pred_list.append(pred)
    with NamedTemporaryFile(mode='w', delete=False, dir=settings.MOLGAN_TMP_DIR) as f:
        json.dump(pred_list, f, indent=4)
        return f.name