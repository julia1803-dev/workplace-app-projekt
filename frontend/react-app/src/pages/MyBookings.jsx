import { useEffect, useState } from "react";
import { deleteBooking, getUserBookings } from "../services/api";

export default function MyBookings({ selectedUser }) {
  const [bookings, setBookings] = useState([]);
  const [message, setMessage] = useState("");

  async function loadBookings() {
    if (!selectedUser) return;
    const data = await getUserBookings(selectedUser.id);
    setBookings(data);
  }

  useEffect(() => {
    loadBookings().catch(console.error);
  }, [selectedUser]);

  async function handleDelete(bookingId) {
    try {
      await deleteBooking(bookingId);
      setMessage("Buchung wurde storniert.");
      await loadBookings();
    } catch (error) {
      setMessage("Buchung konnte nicht storniert werden.");
    }
  }

  if (!selectedUser) {
    return null;
  }

  return (
    <div className="booking-card my-bookings">
      <h3>📋 Meine Buchungen</h3>

      {message && <p className="booking-info">{message}</p>}

      {bookings.length === 0 ? (
        <p>Keine Buchungen vorhanden.</p>
      ) : (
        <div className="my-bookings-list">
          {bookings.map((booking) => (
            <div className="my-booking-item" key={booking.id}>
              <div>
                <strong>Datum:</strong> {booking.booking_date}
                <br />
                <strong>Desk ID:</strong> {booking.desk_id}
              </div>

              <button
                className="delete-button"
                onClick={() => handleDelete(booking.id)}
              >
                Stornieren
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}