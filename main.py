import database as db
import ui

if __name__ == "__main__":
    db.initialize_db()
    ui.main()


try:
    print("Iniciando a aplicação...")
    ui.main()
except Exception as e:
    print(f"Ocorreu um erro: {e}")
    raise
