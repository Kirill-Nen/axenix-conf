from app import app, init_models

#стартер
def start_app(
    host: str = '127.0.0.1',
    port: int = 8000,
    debug: bool = True
):
    init_models()
    app.run(
        host=host,
        port=port,
        debug=debug
    )

    
if __name__ == '__main__':
    start_app()