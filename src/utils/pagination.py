from flask import request

def get_pagination_params():
    limit = int(request.args.get('_limit', 10))
    offset = int(request.args.get('_offset', 0))
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