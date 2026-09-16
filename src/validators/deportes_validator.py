def validar_peticion_deportes(args):
    if args: 
        desconocidos = ", ".join(args.keys())
    raise ValueError(f"Parámetros no permitidos: {desconocidos}")