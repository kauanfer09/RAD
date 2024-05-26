from app import db

class Mission(db.Model): #Criando uma classe chamada Mission
    __tablename__ = "Tabela de Missões" #Mudando o nome da tabela

    #Contruindo o banco de dados
    missionId = db.Column(db.Integer, primary_key=True)
    missionName = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    destiny = db.Column(db.String(30), nullable=False)
    missionState = db.Column(db.String(10), nullable=False)
    missionCrew = db.Column(db.String(100), nullable=False)
    payload = db.Column(db.String(1000), nullable=False)
    duration = db.Column(db.String, nullable=False)
    cost = db.Column(db.Numeric(precision=15, scale=2), nullable=False)
    status = db.Column(db.String, nullable=False)

    #Contruindo o banco de dados VISUAL
    def __init__(self, missionName, date, destiny, missionState, missionCrew, payload, duration, cost, status):
        self.missionName = missionName
        self.date = date
        self.destiny = destiny
        self.missionState = missionState
        self.missionCrew = missionCrew
        self.payload = payload
        self.duration = duration
        self.cost = cost
        self.status = status
