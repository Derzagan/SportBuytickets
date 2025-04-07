  const hall = document.getElementById("hall");
  let selected = [];
  let takenSeats = [];

  // Настройки сцены
  const stageStartRow = 10;
  const stageEndRow = 16;
  const stageStartCol = 8;
  const stageEndCol = 18;

  // Получаем название события из URL
  const urlParams = new URLSearchParams(window.location.search);
  const eventName = urlParams.get("event") || "default";

  // Отрисовка зала
  function renderHall() {
    hall.innerHTML = "";
    for (let row = 1; row <= 25; row++) {
      for (let col = 1; col <= 25; col++) {
        const seatId = `${row}-${col}`;

        // Пропустить место сцены
        if (
          row >= stageStartRow && row <= stageEndRow &&
          col >= stageStartCol && col <= stageEndCol
        ) {
          if (row === stageStartRow && col === stageStartCol) {
            const stage = document.createElement("div");
            stage.className = "stage";
            stage.textContent = "Сцена";
            hall.appendChild(stage);
          }
          continue;
        }

        // Создание места
        const seat = document.createElement("div");
        seat.className = "seat";
        seat.dataset.seat = seatId;

        if (takenSeats.includes(seatId)) {
          seat.classList.add("taken");
        }

        seat.onclick = function () {
          if (seat.classList.contains("taken")) return;
          seat.classList.toggle("selected");
          if (selected.includes(seatId)) {
            selected = selected.filter(s => s !== seatId);
          } else {
            selected.push(seatId);
          }
        };

        hall.appendChild(seat);
      }
    }
  }

  // Получение занятых мест с сервера
  async function loadTakenSeats() {
    const response = await fetch(`/taken_seats?event=${eventName}`);
    const data = await response.json();
    takenSeats = data.taken;
    renderHall();
  }

  // Покупка мест
  async function buySeats() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const dob = document.getElementById("dob").value;

    if (!name || !email || !dob || selected.length === 0) {
      alert("Пожалуйста, заполните все поля и выберите хотя бы одно место.");
      return;
    }

    const payload = {
      name,
      email,
      dob,
      seats: selected,
      event: eventName
    };

    const response = await fetch("/buy", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const result = await response.json();
    alert(result.message);
    selected = [];
    await loadTakenSeats();
  }

  // Загрузка при открытии
  loadTakenSeats();

