export default function (server) {
  server.create("instance", { id: 2 });

  server.create("service", { id: 20032 }); // Amt für Gemeinden und Raumordnung - Abteilung Bauen
  server.create("service", { id: 2 }); // Leitbehörde Burgdorf
  server.create("service", { id: 3 }); // Baukontrolle Burgdorf
  server.create("service", { id: 20003 }); // Leitbehörde Eggiwil
  server.create("service", { id: 20023 }); //Regierungsstatthalteramt Emmental

  server.createList("history-entry", 5, { instanceId: 2 });

  server.createList("journal-entry", 3, { instanceId: 2 });

  server.createList("notification-template", 3);

  // Communications module setup
  server.create("communications-entity", { isApplicant: true });
  server.createList("communications-entity", 4);
  server.createList("instance", 5, "withTopics");
  const attachments = server.createList("communications-attachment", 3);
  attachments.forEach((attachment, index) =>
    attachment.update({
      communicationsMessage: server.schema.communicationsMessages.find(
        index + 1
      ),
    })
  );
}
