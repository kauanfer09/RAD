from flask import render_template, request, redirect, url_for
from app import app, db  # Importa a instância do aplicativo Flask e o objeto do banco de dados SQLAlchemy
from app.models.missions_table import Mission  # Importa o modelo(banco) Mission
from datetime import datetime  # Importa a classe datetime para lidar com datas

# Rota para visualizar todas as missões
@app.route('/')
@app.route('/mission')
def viewMission():
    missions = Mission.query.order_by(Mission.date.desc()).all()  # Consulta todas as missões no banco de dados
    return render_template('mission.html', missions=missions)  # Renderiza o template 'mission.html' passando as missões como contexto


# Rota para visualizar os detalhes das missões
@app.route('/mission/missionDetails/<int:mission_id>')
def viewMissionDetails(mission_id):
    try:
        mission = Mission.query.get(mission_id)
        if mission:
            return render_template('missionDetails.html', mission=mission)  # Certifique-se de que o nome do template é 'missionDetails.html'
        else:
            return render_template('error.html', message='Missão não encontrada.'), 404
    except Exception as e:
        return render_template('error.html', message=f'Erro ao processar solicitação: {str(e)}'), 500


# Rota para pesquisar missões por intervalo de datas
@app.route('/mission/search_date', methods=['GET', 'POST'])
def search_date():
    if request.method == 'POST':  # Se a requisição for do tipo POST, Obtém a data de início e término do formulário
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')  # Converte a data de início para o formato datetime
            end_date = datetime.strptime(end_date, '%Y-%m-%d')  # Converte a data de término para o formato datetime
        except ValueError as e:
            return render_template('error.html', message=f'Formato de data inválido: {str(e)}'), 400  # Renderiza o template 'error.html' com uma mensagem de erro se o formato da data for inválido

        missions = Mission.query.filter(Mission.date.between(start_date, end_date)).all()  # Consulta as missões dentro do intervalo de datas
        return render_template('search_date.html', missions=missions)  # Renderiza o template 'search_date.html' passando as missões como contexto
    return render_template('search_date_form.html')  # Se a requisição não for do tipo POST, renderiza o formulário para pesquisar por datas


# Rota para pesquisar uma missão por ID
@app.route('/search_by_id', methods=['GET', 'POST'])
def search_mission_by_id():
    if request.method == 'POST':  # Se a requisição for do tipo POST
        mission_id = request.form['mission_id']  # Obtém o ID da missão do formulário
        mission = Mission.query.get(mission_id)  # Consulta a missão pelo ID
        if mission:
            return render_template('missionDetails.html', mission=mission)  # Certifique-se de que o nome do template é 'missionDetails.html'
        else:
            return render_template('error.html', message='Missão não encontrada.'), 404  # Renderiza o template 'error.html' com uma mensagem de erro se a missão não for encontrada
    return render_template('search_by_id.html')  # Se a requisição não for do tipo POST, renderiza o formulário para pesquisar por ID


# Rota para adicionar uma nova missão
@app.route('/adicionar_missao', methods=['GET', 'POST'])
def adicionar_missao():
    if request.method == 'POST':  # Se a requisição for do tipo POST
        try:
            nova_missao = Mission(  # Cria uma nova instância de Mission com os dados do formulário
                missionName=request.form['missionName'],
                date=datetime.strptime(request.form['date'], '%Y-%m-%d'),
                destiny=request.form['destiny'],
                missionState=request.form['missionState'],
                missionCrew=request.form['missionCrew'],
                payload=request.form['payload'],
                duration=request.form['duration'],
                cost=request.form['cost'],
                status=request.form['status']
            )

            db.session.add(nova_missao)  # Adiciona a nova missão ao banco de dados
            db.session.commit()  #Confirma a alteração
            return redirect(url_for('viewMission'))  #Redireciona para a página de visualização de missões
        except Exception as e:
            db.session.rollback()  # Em caso de erro, não irá adicionar
            return f"Erro ao adicionar a missão: {str(e)}"  #Retorna uma mensagem de erro
    return render_template('adicionar_missao.html')  #Se a requisição não for do tipo POST, renderiza o formulário para adicionar uma nova missão

# Rota feita para editar uma missão já existente
@app.route('/mission/edit_mission/<int:mission_id>', methods=['GET', 'POST'])
def edit_mission(mission_id):
    try:
        mission = Mission.query.get(mission_id)
        if not mission:
            return render_template('error.html', message='Missão não encontrada.'), 404
        
        if request.method == 'POST':
            try:
                mission.missionName = request.form['missionName']
                mission.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
                mission.destiny = request.form['destiny']
                mission.missionState = request.form['missionState']
                mission.missionCrew = request.form['missionCrew']
                mission.payload = request.form['payload']
                mission.duration = request.form['duration']
                mission.cost = request.form['cost']
                mission.status = request.form['status']
                
                db.session.commit()
                return redirect(url_for('viewMissionDetails', mission_id=mission.missionId))
            except Exception as e:    
                db.session.rollback() #Em caso de erro, desfaz a mudança
                return render_template('error.html', message=f'Erro ao atualizar a missão: {str(e)}'), 500
            
        return render_template('editMission.html', mission=mission)
    except Exception as e:
        return render_template('error.html', message=f'Erro ao atualizar a missão: {str(e)}'), 500

#Rota para excluir uma missão utilizando seu ID. 
@app.route('/mission/delete/<int:mission_id>', methods = ['POST'])
def delete_mission(mission_id):
    try:
        mission = Mission.query.get(mission_id)
        if not mission:
            return render_template('error.html', message='Missão não encontrada.'), 404

        db.session.delete(mission) #Exclui a missão do banco de dados
        db.session.commit() #Confirma a exclusão
        return redirect(url_for('viewMission')) #Retorna para a página de visualização de missões
    except Exception as e:
        db.session.rollback() #Em caso de erro, não irá deletar
        return render_template('error.html', message=f'Não foi possível deletar a missão: {str(e)}'), 500
