from flask import Blueprint, render_template, request, redirect, url_for, flash
from sentence_transformers import SentenceTransformer, util
from config import Config
from data_handler import get_all_smartphones, get_smartphone_by_id, get_unique_values

rec_bp = Blueprint('recommendation', __name__, url_prefix='/recommend')

# Initialize embedding model once
d_model = SentenceTransformer(Config.MODEL_NAME)

@rec_bp.route('/select', methods=['GET', 'POST'])
def recommend_from_select():
    # GET: show select box
    if request.method == 'GET':
        smartphones = get_all_smartphones()
        return render_template('user/recommendation1.html', smartphones=smartphones)
    # POST: process selection
    smartphone_id = request.form.get('smartphone_id')
    if not smartphone_id:
        flash('Please select a smartphone.', 'warning')
        return redirect(url_for('recommendation.recommend_from_select'))
    entry = get_smartphone_by_id(smartphone_id)
    input_text = entry['specification']
    return _compute_and_render(input_text, exclude_id=int(smartphone_id))

@rec_bp.route('/manual', methods=['GET', 'POST'])
def recommend_from_manual():
    # GET: show manual input form
    if request.method == 'GET':
        data = {
            'brands': get_unique_values('brand'),
            'chipsets': get_unique_values('chipset'),
            'rams': get_unique_values('ram'),
            'storages': get_unique_values('storage'),
            'batteries': get_unique_values('battery'),
            'cameras': get_unique_values('main_camera'),
            'sizes': get_unique_values('size'),
            'lcds': get_unique_values('lcd'),
            'signals': get_unique_values('band_1'),
            'years': get_unique_values('release_year')
        }
        return render_template('user/recommendation2.html', **data)
    # POST: process manual input
    parts = [
        request.form.get('brand', ''),
        request.form.get('chipset', ''),
        f"{request.form.get('ram', '')} RAM" if request.form.get('ram') else '',
        f"{request.form.get('storage', '')} Storage" if request.form.get('storage') else '',
        request.form.get('battery', ''),
        request.form.get('main_camera', ''),
        f"{request.form.get('size', '')}-inch" if request.form.get('size') else '',
        request.form.get('lcd', ''),
        request.form.get('band_1', ''),
        request.form.get('release_year', '')
    ]
    input_text = ' '.join([p for p in parts if p])
    if not input_text:
        flash('Please fill at least one field.', 'warning')
        return redirect(url_for('recommendation.recommend_from_manual'))
    return _compute_and_render(input_text)


def _compute_and_render(input_text, exclude_id=None):
    all_phones = get_all_smartphones()
    specs = [p['specification'] for p in all_phones if p['specification']]
    embeddings = d_model.encode(specs, convert_to_tensor=True)
    query_emb = d_model.encode(input_text, convert_to_tensor=True)
    sims = util.pytorch_cos_sim(query_emb, embeddings)[0]
    sorted_idx = sims.argsort(descending=True).tolist()
    if exclude_id is not None:
        sorted_idx = [i for i in sorted_idx if all_phones[i]['id'] != exclude_id]
    recommendations = [(all_phones[i], sims[i].item()) for i in sorted_idx[:5]]
    return render_template('user/result.html', recommendations=recommendations)