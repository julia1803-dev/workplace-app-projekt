from typing import Optional #Wert kann vorhanden sein oder None
from datetime import date
from sqlmodel import SQLModel, Field #Basis für Datenbankmodelle und Field beschreibt Datenbankspalten


class Team(SQLModel, table=True): #Vererbung, Klasse soll eine Datenbanktabelle werden
    id: Optional[int] = Field(default=None, primary_key=True) #Primärschlüssel, Attribut der Klasse
    name: str #Teamname, Attribut


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    team_id: Optional[int] = Field(default=None, foreign_key="team.id") #Fremdschlüssel


class Zone(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Desk(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str
    zone_id: Optional[int] = Field(default=None, foreign_key="zone.id")


class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id") #wer bucht
    desk_id: int = Field(foreign_key="desk.id") #welcher Platz
    booking_date: date
    status: str = "active"


class BookingCreate(SQLModel):
    user_id: int
    desk_id: int
    booking_date: date