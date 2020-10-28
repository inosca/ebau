export default function (server) {
  server.create("service", { id: 20032 }); // Amt für Gemeinden und Raumordnung - Abteilung Bauen
  server.create("service", { id: 2 }); // Leitbehörde Burgdorf
  server.create("service", { id: 3 }); // Baukontrolle Burgdorf
  server.create("service", { id: 20003 }); // Leitbehörde Eggiwil
  server.create("service", { id: 20023 }); //Regierungsstatthalteramt Emmental

  server.createList("history-entry", 5, { instanceId: 2 });

  server.createList("journal-entry", 3, { instanceId: 2 });
}
