from flask import request

DEFAULT_LIMIT = 10
MIN_LIMIT = 1
MAX_LIMIT = 100
MIN_OFFSET = 0

def get_pagination_params():
    try:  
        limit = int(request.args.get('_limit', DEFAULT_LIMIT))
        offset = int(request.args.get('_offset', MIN_OFFSET))
    except ValueError:
        raise ValueError("Los parámetros '_limit' y '_offset' deben ser números enteros.")

    if not (MIN_LIMIT <= limit <= MAX_LIMIT):
        raise ValueError(f"El parámetro '_limit' debe estar entre {MIN_LIMIT} y {MAX_LIMIT}.")

    if offset < MIN_OFFSET:
        raise ValueError(f"El parámetro '_offset' debe ser mayor o igual a {MIN_OFFSET}.")

    return limit, offset

def generate_hateoas_links(base_url, limit, offset, total_records, request_args):
    links = {}

    filtros_str = "".join([f"&{k}={v}" for k, v in request_args.items() if k not in ['_limit', '_offset']])
    
    links["_first"] = {"href": f"{base_url}?_limit={limit}&_offset=0{filtros_str}"}
    
    if offset > 0:
        prev_offset = max(0, offset - limit)
        links["_prev"] = {"href": f"{base_url}?_limit={limit}&_offset={prev_offset}{filtros_str}"}
        
    if offset + limit < total_records:
        links["_next"] = {"href": f"{base_url}?_limit={limit}&_offset={offset + limit}{filtros_str}"}
        
    if total_records > 0:
        last_offset = ((total_records - 1) // limit) * limit
        links["_last"] = {"href": f"{base_url}?_limit={limit}&_offset={last_offset}{filtros_str}"}
    else:
        links["_last"] = {"href": f"{base_url}?_limit={limit}&_offset=0{filtros_str}"}
        
    return links