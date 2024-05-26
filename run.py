from app import app         #Importando a instância do aplicativo Flask criada no arquivo `app.py`.

if __name__ == "__main__":  #Verificando se este arquivo está sendo executado como o programa principal.
    app.run(debug=True)     #Inicia o servidor de desenvolvimento embutido do Flask.

