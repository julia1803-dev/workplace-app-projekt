from fastapi import APIRouter, Depends, HTTPException 
from sqlmodel import Session, select #Session - Datenbankverbindung, select Datenbankabfragen
from datetime import date
from app.database import engine #Verbindung zur DB
from app.models import BookingCreate, Team, Zone, Desk, Booking, User #Models - Tabellen
from app.services import BookingService #Geschäftslogik
import traceback #Debugging

router = APIRouter()


def get_session():
    with Session(engine) as session: #Öffnung Verbindung
        yield session #gibt Session weiter


# 🔹 CREATE BOOKING
@router.post("/bookings/") #Daten erstellen
def create_booking(booking: BookingCreate, session: Session = Depends(get_session)):
    try:
        return BookingService.create_booking(session, booking)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) #falsche Eingabe
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e)) #Serverfehler

# 🔹 GET BOOKINGS BY USER 
#  
@router.get("/bookings/user/{user_id}")
def get_user_bookings(user_id: int, session: Session = Depends(get_session)):
    bookings = session.exec(
        select(Booking).where(Booking.user_id == user_id)
    ).all()
    return bookings

# 🔹 DELETE BOOKING
@router.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, session: Session = Depends(get_session)):
    booking = session.get(Booking, booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Buchung wurde nicht gefunden.")

    session.delete(booking)
    session.commit()

    return {"message": "Buchung wurde storniert."}


# 🔹 TEAMS
@router.get("/teams/")
def get_teams(session: Session = Depends(get_session)):
    return session.exec(select(Team)).all() #alle Teams holen


# 🔹 ZONES
@router.get("/zones/")
def get_zones(session: Session = Depends(get_session)):
    return session.exec(select(Zone)).all() #alle Zone holen


# 🔹 DESKS PER ZONE
@router.get("/desks/{zone_id}")
def get_desks(zone_id: int, session: Session = Depends(get_session)):
    return session.exec(
        select(Desk).where(Desk.zone_id == zone_id) #alle Arbeitsplätze holen
    ).all()


# 🔹 ZONE STATUS (gesamt)
@router.get("/zone-status/") #Wie viele Plätze frei oder besetzt
def get_zone_status(zone_id: int, booking_date: date, session: Session = Depends(get_session)):
    desks = session.exec(
        select(Desk).where(Desk.zone_id == zone_id)
    ).all()

    total_desks = len(desks)
    desk_ids = [desk.id for desk in desks]

    if not desk_ids:
        return {
            "zone_id": zone_id,
            "booking_date": booking_date,
            "total_desks": 0,
            "occupied_desks": 0,
            "free_desks": 0
        }

    bookings = session.exec(
        select(Booking).where(
            Booking.booking_date == booking_date,
            Booking.desk_id.in_(desk_ids)
        )
    ).all()

    occupied_desks = len(bookings)
    free_desks = total_desks - occupied_desks

    return {
        "zone_id": zone_id,
        "booking_date": booking_date,
        "total_desks": total_desks,
        "occupied_desks": occupied_desks,
        "free_desks": free_desks
    }


# 🔹 ZONE DETAIL (freie + besetzte desks)
@router.get("/zone-desks-status/") #freie und belegte Plätze
def get_zone_desks_status(zone_id: int, booking_date: date, session: Session = Depends(get_session)):
    desks = session.exec(
        select(Desk).where(Desk.zone_id == zone_id)
    ).all()

    desk_ids = [desk.id for desk in desks]

    if not desk_ids:
        return {
            "zone_id": zone_id,
            "booking_date": booking_date,
            "free_desks": [],
            "occupied_desks": []
        }

    bookings = session.exec(
        select(Booking).where(
            Booking.booking_date == booking_date,
            Booking.desk_id.in_(desk_ids)
        )
    ).all()

    occupied_ids = {booking.desk_id for booking in bookings} #Set für schnelle Suche

    free_desks = []
    occupied_desks = []

    for desk in desks:
        if desk.id in occupied_ids:
            occupied_desks.append({"id": desk.id, "code": desk.code}) #besetzte Plätze hinzufügen
        else:
            free_desks.append({"id": desk.id, "code": desk.code}) #freie Plätze hinzufügen

    return {
        "zone_id": zone_id,
        "booking_date": booking_date,
        "free_desks": free_desks,
        "occupied_desks": occupied_desks
    }


@router.get("/users/by-team/{team_id}") #alle Users eines Teams
def get_users_by_team(team_id: int, session: Session = Depends(get_session)):
    return session.exec(
        select(User).where(User.team_id == team_id)
    ).all()