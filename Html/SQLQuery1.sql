CREATE TABLE Tickets (
    Id INT IDENTITY PRIMARY KEY,
    EventName NVARCHAR(100),
    SeatRow INT,
    SeatCol INT,
    FullName NVARCHAR(100),
    Email NVARCHAR(100),
    DateBirth DATE
);
