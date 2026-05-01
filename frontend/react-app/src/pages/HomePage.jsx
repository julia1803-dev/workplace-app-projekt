import { useEffect, useMemo, useState } from "react";
import "./home.css";
import MyBookings from "./MyBookings";
import {
  getTeams,
  getUsersByTeam,
  getZones,
  getZoneStatus,
  getZoneDesksStatus,
  createBooking,
} from "../services/api";

function formatDateForInput(value) {
  return value.toISOString().split("T")[0];
}

export default function HomePage() {
  const [teams, setTeams] = useState([]);
  const [users, setUsers] = useState([]);
  const [zones, setZones] = useState([]);

  const [selectedTeamId, setSelectedTeamId] = useState("");
  const [selectedUserId, setSelectedUserId] = useState("");
  const [selectedZoneId, setSelectedZoneId] = useState("");
  const [selectedDate, setSelectedDate] = useState(formatDateForInput(new Date()));

  const [zoneStatus, setZoneStatus] = useState(null);
  const [zoneDeskStatus, setZoneDeskStatus] = useState(null);

  const [selectedDeskId, setSelectedDeskId] = useState("");
  const [loading, setLoading] = useState(true);
  const [bookingMessage, setBookingMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadInitialData() {
      try {
        setLoading(true);
        const [teamsData, zonesData] = await Promise.all([getTeams(), getZones()]);
        setTeams(teamsData);
        setZones(zonesData);

        if (teamsData.length > 0) setSelectedTeamId(String(teamsData[0].id));
        if (zonesData.length > 0) setSelectedZoneId(String(zonesData[0].id));
      } catch (error) {
        setErrorMessage("Daten konnten nicht geladen werden.");
      } finally {
        setLoading(false);
      }
    }

    loadInitialData();
  }, []);

  useEffect(() => {
    async function loadUsers() {
      if (!selectedTeamId) return;

      try {
        const usersData = await getUsersByTeam(selectedTeamId);
        setUsers(usersData);

        if (usersData.length > 0) {
          setSelectedUserId(String(usersData[0].id));
        } else {
          setSelectedUserId("");
        }
      } catch (error) {
        setErrorMessage("Benutzer konnten nicht geladen werden.");
      }
    }

    loadUsers();
  }, [selectedTeamId]);

  async function loadZoneData() {
    if (!selectedZoneId || !selectedDate) return;

    const [statusData, deskData] = await Promise.all([
      getZoneStatus(selectedZoneId, selectedDate),
      getZoneDesksStatus(selectedZoneId, selectedDate),
    ]);

    setZoneStatus(statusData);
    setZoneDeskStatus(deskData);
  }

  useEffect(() => {
    loadZoneData().catch(() => {
      setErrorMessage("Zonenstatus konnte nicht geladen werden.");
    });
  }, [selectedZoneId, selectedDate]);

  const freeDesks = useMemo(() => zoneDeskStatus?.free_desks ?? [], [zoneDeskStatus]);
  const occupiedDesks = useMemo(() => zoneDeskStatus?.occupied_desks ?? [], [zoneDeskStatus]);

  const selectedUser = useMemo(
    () => users.find((user) => String(user.id) === selectedUserId),
    [users, selectedUserId]
  );

  useEffect(() => {
    if (freeDesks.length > 0) {
      setSelectedDeskId(String(freeDesks[0].id));
    } else {
      setSelectedDeskId("");
    }
  }, [freeDesks]);

  async function handleBooking() {
    if (!selectedUserId || !selectedDeskId || !selectedDate) {
      setErrorMessage("Bitte alle Felder auswählen.");
      return;
    }

    try {
      setBookingMessage("");
      setErrorMessage("");

      await createBooking({
        user_id: Number(selectedUserId),
        desk_id: Number(selectedDeskId),
        booking_date: selectedDate,
      });

      setBookingMessage("Buchung erfolgreich!");
      await loadZoneData();
    } catch (error) {
      setErrorMessage("Buchung konnte nicht durchgeführt werden.");
    }
  }

  async function handleCheckAvailability() {
    try {
      setBookingMessage("");
      setErrorMessage("");
      await loadZoneData();
      setBookingMessage("Verfügbarkeit aktualisiert!");
    } catch (error) {
      setErrorMessage("Fehler beim Laden der Verfügbarkeit.");
    }
  }

  if (loading) {
    return (
      <div className="app">
        <p>Lade Daten...</p>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="header">🏢 Workplace Booking</div>

      <div className="hero">
        <h2>Teamanwesenheiten im Büro</h2>
        <p>Heute im Büro</p>
      </div>

      <p className="intro">
        Wähle Team, Mitarbeiter, Zone und Datum aus, prüfe die Verfügbarkeit und buche einen Arbeitsplatz.
      </p>

      {errorMessage && <div className="message error">{errorMessage}</div>}
      {bookingMessage && <div className="message success">{bookingMessage}</div>}

      <div className="form-grid">
        <div className="field">
          <label>Team</label>
          <select value={selectedTeamId} onChange={(e) => setSelectedTeamId(e.target.value)}>
            {teams.map((team) => (
              <option key={team.id} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label>Mitarbeiter</label>
          <select value={selectedUserId} onChange={(e) => setSelectedUserId(e.target.value)}>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label>Datum</label>
          <input type="date" value={selectedDate} onChange={(e) => setSelectedDate(e.target.value)} />
        </div>
      </div>

      <div className="field zone-field">
        <label>Zone</label>
        <select value={selectedZoneId} onChange={(e) => setSelectedZoneId(e.target.value)}>
          {zones.map((zone) => (
            <option key={zone.id} value={zone.id}>
              {zone.name}
            </option>
          ))}
        </select>
      </div>

      <div className="stats-section">
        <h3>📊 Belegung der Zone</h3>
        <div className="stats-grid">
          <div className="stat-card">
            <span>Gesamtplätze</span>
            <strong>{zoneStatus?.total_desks ?? 0}</strong>
          </div>
          <div className="stat-card">
            <span>Besetzt</span>
            <strong>{zoneStatus?.occupied_desks ?? 0}</strong>
          </div>
          <div className="stat-card">
            <span>Frei</span>
            <strong>{zoneStatus?.free_desks ?? 0}</strong>
          </div>
        </div>
      </div>

      <div className="desk-columns">
        <div className="desk-card light">
          <h3>✅ Freie Arbeitsplätze</h3>
          {freeDesks.length > 0 ? (
            <div className="desk-list">
              {freeDesks.map((desk) => (
                <span className="desk-chip free" key={desk.id}>
                  {desk.code}
                </span>
              ))}
            </div>
          ) : (
            <p>Keine freien Arbeitsplätze</p>
          )}
        </div>

        <div className="desk-card light">
          <h3>❌ Besetzte Arbeitsplätze</h3>
          {occupiedDesks.length > 0 ? (
            <div className="desk-list">
              {occupiedDesks.map((desk) => (
                <span className="desk-chip occupied" key={desk.id}>
                  {desk.code}
                </span>
              ))}
            </div>
          ) : (
            <p>Keine besetzten Arbeitsplätze</p>
          )}
        </div>
      </div>

      <div className="booking-card">
        <h3>🪑 Arbeitsplatz buchen</h3>

        <div className="field">
          <label>Freien Arbeitsplatz auswählen</label>
          <select
            value={selectedDeskId}
            onChange={(e) => setSelectedDeskId(e.target.value)}
            disabled={freeDesks.length === 0}
          >
            {freeDesks.length === 0 ? (
              <option value="">Keine freien Arbeitsplätze</option>
            ) : (
              freeDesks.map((desk) => (
                <option key={desk.id} value={desk.id}>
                  {desk.code}
                </option>
              ))
            )}
          </select>
        </div>

        <div className="buttons">
          <button className="primary" onClick={handleBooking} disabled={!selectedDeskId}>
            Arbeitsplatz buchen
          </button>

          <button className="secondary" type="button" onClick={handleCheckAvailability}>
            Verfügbarkeit prüfen
          </button>
        </div>
      </div>

      <MyBookings selectedUser={selectedUser} />
    </div>
  );
}