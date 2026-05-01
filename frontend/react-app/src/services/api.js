const API_URL = "https://workplace-app-aqsv.onrender.com";

async function handleResponse(response) {
  if (!response.ok) {
    throw new Error(`API Fehler: ${response.status}`);
  }
  return response.json();
}

export async function getTeams() {
  const response = await fetch(`${API_URL}/teams/`);
  return handleResponse(response);
}

export async function getUsersByTeam(teamId) {
  const response = await fetch(`${API_URL}/users/by-team/${teamId}`);
  return handleResponse(response);
}

export async function getZones() {
  const response = await fetch(`${API_URL}/zones/`);
  return handleResponse(response);
}

export async function getZoneStatus(zoneId, bookingDate) {
  const response = await fetch(
    `${API_URL}/zone-status/?zone_id=${zoneId}&booking_date=${bookingDate}`
  );
  return handleResponse(response);
}

export async function getZoneDesksStatus(zoneId, bookingDate) {
  const response = await fetch(
    `${API_URL}/zone-desks-status/?zone_id=${zoneId}&booking_date=${bookingDate}`
  );
  return handleResponse(response);
}

export async function createBooking(data) {
  const response = await fetch(`${API_URL}/bookings/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return handleResponse(response);
}

export async function getUserBookings(userId) {
  const response = await fetch(`${API_URL}/bookings/user/${userId}`);
  return handleResponse(response);
}

export async function deleteBooking(bookingId) {
  const response = await fetch(`${API_URL}/bookings/${bookingId}`, {
    method: "DELETE",
  });
  return handleResponse(response);
}