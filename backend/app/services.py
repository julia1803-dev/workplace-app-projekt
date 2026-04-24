from sqlmodel import Session, select #Session - Verbindung zur Datenbank, select - Daten abfragen
from app.models import Booking, BookingCreate, User, Desk #Booking - Tabelle, BookingCreate - Eingabedaten


class BookingService: #enthält alle Funktionen bzgl. Buchungen
    @staticmethod #die Methode gehört zur Klasse, aber braucht kein Objekt
    def create_booking(session: Session, booking_data: BookingCreate):
        user = session.get(User, booking_data.user_id) #user prüfen
        if not user:
            raise ValueError("User wurde nicht gefunden.")

        desk = session.get(Desk, booking_data.desk_id) #desk prüfen
        if not desk:
            raise ValueError("Arbeitsplatz wurde nicht gefunden.")

        existing = session.exec(
            select(Booking).where(
                Booking.desk_id == booking_data.desk_id,
                Booking.booking_date == booking_data.booking_date
            ) #Doppelbuchung verhindern
        ).first()

        if existing:
            raise ValueError("Arbeitsplatz ist an diesem Datum bereits gebucht.")

        booking = Booking(
            user_id=booking_data.user_id,
            desk_id=booking_data.desk_id,
            booking_date=booking_data.booking_date
        ) #Buchung erstellen

        session.add(booking)
        session.commit()
        session.refresh(booking) #ID holen
        return booking #API bekommt Ergebnis

    @staticmethod
    def delete_booking(session: Session, booking_id: int):
        booking = session.get(Booking, booking_id) #Buchung suchen
        if not booking:
            raise ValueError("Buchung wurde nicht gefunden.")

        session.delete(booking)
        session.commit()