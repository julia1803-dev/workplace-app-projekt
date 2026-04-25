import random
from sqlmodel import Session, select #Session - Verbindung zur Datenbank, select - Daten abfragen
from app.database import engine, create_db #DB-Verbindung, create_db - erstellt Tabellen
from app.models import Team, User, Zone, Desk


def seed_data(): #erstellt alle Testdaten
    create_db() #Tabellen werden erstellt

    with Session(engine) as session:
        existing_team = session.exec(select(Team)).first() #erstes Team aus der DB
        if existing_team:
            print("Seed-Daten schon vorhanden.") #verhindert doppelte Dateien
            return

        team_names = [
            "Eiger", "Gurten", "Titlis", "Matterhorn", "Mönch",
            "Weisshorn", "Dom", "Rothorn", "Niesen",
            "Niederhorn", "Pilatus", "Stockhorn", "Brisen"
        ]

        user_names_by_team = {
            "Eiger": ["Anna Keller", "Marco Huber", "Sophie Meier", "Luca Steiner", "Nina Frei"],
            "Gurten": ["Lukas Graf", "Nina Berger", "Tobias Frei", "Jan Müller", "Sara Koch"],
            "Titlis": ["Lea Schmid", "David Weber", "Mia Baumann", "Noah Meier", "Laura Graf"],
            "Matterhorn": ["Noah Koch", "Sara Moser", "Jan Hofer", "Tim Keller", "Clara Weber"],
            "Mönch": ["Elin Walter", "Jonas Ziegler", "Clara Roth", "Fabian Huber", "Lena Frei"],
            "Weisshorn": ["Tim Wyss", "Laura Bühler", "Ben Ammann", "Mia Keller", "Nico Graf"],
            "Dom": ["Mila Gerber", "Simon Kuhn", "Jana Suter", "Lina Meier", "David Roth"],
            "Rothorn": ["Lena Marti", "Fabian Gross", "Nora Egli", "Jonas Frei", "Sara Weber"],
            "Niesen": ["Joel Haller", "Eva Christen", "Liv Fuchs", "Tim Schmid", "Anna Graf"],
            "Niederhorn": ["Finn Stadelmann", "Lia Jost", "Eric Haas", "Clara Meier", "Noah Frei"],
            "Pilatus": ["Mara Vogel", "Janis Maurer", "Paula Steck", "Luca Huber", "Nina Roth"],
            "Stockhorn": ["Livia Brunner", "Nico Bär", "Alina Kunz", "Sara Keller", "Jonas Graf"],
            "Brisen": ["Silas Etter", "Mira Kessler", "Yann Wick", "Tim Frei", "Laura Meier"]
        }

        first_names = [
            "Anna", "Marco", "Sophie", "Luca", "Nina", "Lukas", "Tobias", "Lea",
            "David", "Mia", "Noah", "Sara", "Jan", "Tim", "Clara", "Jonas",
            "Laura", "Fabian", "Lena", "Joel", "Eva", "Liv", "Finn", "Lia",
            "Eric", "Mara", "Paula", "Silas", "Mira", "Yann"
        ]

        last_names = [
            "Keller", "Huber", "Meier", "Steiner", "Frei", "Graf", "Berger",
            "Schmid", "Weber", "Baumann", "Koch", "Moser", "Hofer", "Wyss",
            "Bühler", "Ammann", "Gerber", "Kuhn", "Suter", "Marti", "Gross",
            "Egli", "Haller", "Christen", "Fuchs", "Jost", "Haas", "Vogel",
            "Maurer", "Brunner", "Kunz", "Etter", "Kessler", "Wick"
        ]

        def generate_more_names(existing_names, target_count=25): #Kopie der vorhandenen Namen
            """
            Erweitert eine Liste von Namen bis zur gewünschten Anzahl.

            - Generiert zufällige Namen aus Vor- und Nachnamen
            - Verhindert doppelte Namen
            - Gibt eine neue Liste zurück

            :param existing_names: Liste vorhandener Namen
            :param target_count: Zielanzahl (Standard: 25)
            :return: Liste mit erweiterten Namen
            """
            names = list(existing_names) 
                    

            while len(names) < target_count: #Schleife läuft so lange, bis genügend Namen vorhanden sind
                new_name = f"{random.choice(first_names)} {random.choice(last_names)}"

                if new_name not in names: #Duplikate vermeiden
                   names.append(new_name)

            return names
        
        for team_name in user_names_by_team: #Schleife über alle Teams
            user_names_by_team[team_name] = generate_more_names(
                user_names_by_team[team_name],
                target_count=25 #Für jedes Team Namen auf 25 auffüllen
            )
        #Ergebnis wird wieder im Dictionary gespeichert

        teams = []
        for name in team_names:
            team = Team(name=name) #Teamobjekt erstellen
            session.add(team) #zur DB hinzufügen
            teams.append(team) #speichern

        session.commit() # die Daten in DB schreiben

        for team in teams:
            session.refresh(team) #id für Teams

        for team in teams:
            names = user_names_by_team.get(team.name, []) #User holen
            for name in names:
                user = User(name=name, team_id=team.id) #Verbindung User mit Team
                session.add(user)

        session.commit() #speichern

        zone_names = [
            "Emme", "Aare", "Brinzersee", "Thunersee",
            "Rhein", "Rhone", "Saane", "Inn"
        ]

        zones = []
        for name in zone_names:
            zone = Zone(name=name) #Zone Objekte erstellen
            session.add(zone)
            zones.append(zone)

        session.commit()

        for zone in zones:
            session.refresh(zone) #die automatisch generierten IDs aus der Datenbank geladen werden

        for zone in zones:
            for i in range(1, 21):
                desk = Desk(
                    code=f"{zone.name[:3].upper()}-{i}", #Drei grosse Buchstaben und -1 bis 20
                    zone_id=zone.id #desk gehört zur Zone
                )
                session.add(desk)

        session.commit()

        print("✅ Realistische Testdaten erstellt!")


if __name__ == "__main__": #Wenn Datei direkt gestartet wird → Daten werden erstellt
    seed_data()