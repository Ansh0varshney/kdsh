from async_actor_critic import async_actor_critic_reasoning
@app.post('/analyze-async')
async def analyze_async(paper_id: int):
    paper_text = get_paper(paper_id)
    if not paper_text:
        return JSONResponse(status_code=404, content={'error': 'Paper not found'})
    result = await async_actor_critic_reasoning(paper_text)
    return {'paper_id': paper_id, 'pipeline': 'ASYNC-ACTOR-CRITIC', 'result': result}

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pipelines import bert_pipeline, basic_llm_pipeline, actor_critic_pipeline, tacc_pipeline
from scribe import scribe_ensemble
from database import add_paper, get_paper, get_all_papers, init_db

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Automated Research Paper Analysis & Conference Recommendation System'}


@app.post('/upload-paper')
async def upload_paper(file: UploadFile = File(...)):
    content = (await file.read()).decode(errors='ignore')
    paper_id = add_paper(file.filename, content)
    return {'filename': file.filename, 'paper_id': paper_id}



@app.post('/analyze')
async def analyze_paper(paper_id: int, pipeline: str = 'BERT'):
    paper_text = get_paper(paper_id)
    if not paper_text:
        return JSONResponse(status_code=404, content={'error': 'Paper not found'})
    pipeline = pipeline.upper()
    if pipeline == 'BERT':
        result = bert_pipeline(paper_text)
    elif pipeline == 'BASIC':
        result = basic_llm_pipeline(paper_text)
    elif pipeline == 'ACTOR-CRITIC':
        result = actor_critic_pipeline(paper_text)
    elif pipeline == 'TACC':
        result = tacc_pipeline(paper_text)
    elif pipeline == 'SCRIBE':
        result = scribe_ensemble(paper_text)
    else:
        result = {'error': 'Pipeline not implemented'}
    return {'paper_id': paper_id, 'pipeline': pipeline, 'result': result}


# Simple conference recommendation based on keyword matching
@app.get('/recommend')
async def recommend_conferences(paper_id: int):
    paper_text = get_paper(paper_id)
    if not paper_text:
        return JSONResponse(status_code=404, content={'error': 'Paper not found'})
    # Example conference topics
    conferences = [
        {'name': 'NeurIPS', 'keywords': ['machine learning', 'deep learning', 'AI']},
        {'name': 'ACL', 'keywords': ['natural language processing', 'NLP', 'linguistics']},
        {'name': 'CVPR', 'keywords': ['computer vision', 'image', 'video']},
        {'name': 'ICRA', 'keywords': ['robotics', 'automation', 'control']},
        {'name': 'STOC', 'keywords': ['theory', 'algorithms', 'complexity']},
    ]
    matches = []
    for conf in conferences:
        for kw in conf['keywords']:
            if kw.lower() in paper_text.lower():
                matches.append(conf['name'])
                break
    return {'paper_id': paper_id, 'conferences': list(set(matches))}
