
const user = result.data;
const updateText = (id, val) => {
  const el = document.getElementById(id);
  if (el) el.textContent = val || "—";
};
const useri = user;

// Basic info
updateText("userId", useri.user_id);
updateText("name", useri.name);
updateText("email", useri.email);
updateText("contact", useri.contact);
updateText(
  "timestamp",
  useri.timestamp ? new Date(useri.timestamp).toLocaleString() : "—"
);
updateText("department", useri.department);
updateText("designation", useri.designation);

// Address
updateText("house_no", useri.house_no);
updateText("block", useri.block);
updateText("city", useri.city);
updateText("state", useri.state);
updateText("pincode", useri.pincode);

// Vehicles
const vehicleContainer = document.getElementById("vehicleList");
const noVehicles = document.getElementById("noVehicles");

if (!useri.vehicles || useri.vehicles.length === 0) {
  if (noVehicles) noVehicles.style.display = "block";
} else {
  useri.vehicles.forEach(v => {
    const card = document.createElement("div");

    card.style.background = "#f9fafb";
    card.style.border = "1px solid #e5e7eb";
    card.style.borderRadius = "10px";
    card.style.padding = "15px";
    card.style.marginBottom = "10px";

    card.innerHTML = `
      <div style="font-weight:700;font-size:15px;">
        🚘 ${v.vehicle_no || "—"}
      </div>
      <div style="font-size:13px;color:#6b7280;margin-top:6px;">
        Type: ${v.vehicle_type || "—"}
      </div>
    `;

    vehicleContainer.appendChild(card);
  });
}
