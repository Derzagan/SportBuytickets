function buySeats() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const dob = document.getElementById("dob").value;
  const eventName = new URLSearchParams(window.location.search).get("event") || "default";

  if (!name || !email || !dob || selected.length === 0) {
    alert("Заполните все поля и выберите места!");
    return;
  }

  selected.forEach(seat => {
    db.collection("tickets").add({
      FullName: name,
      Email: email,
      DateBirth: dob,
      EventName: eventName,
      Seat: seat
    });
  });

  alert("Данные успешно отправлены!");
  selected = [];
}
