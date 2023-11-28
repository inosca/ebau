export default function (server) {
  server.create("service", { id: 20032 }); // Amt für Gemeinden und Raumordnung - Abteilung Bauen
  server.create("service", { id: 2 }); // Leitbehörde Burgdorf
  server.create("service", { id: 3 }); // Baukontrolle Burgdorf
  server.create("service", { id: 20003 }); // Leitbehörde Eggiwil
  server.create("service", { id: 20023 }); //Regierungsstatthalteramt Emmental

  // server.createList("history-entry", 5, { instanceId: 2 });

  // server.createList("journal-entry", 3, { instanceId: 2 });

  server.createList("notification-template", 3);

  server.create("access-level", {
    slug: "service",
    requiredGrantType: "SERVICE",
  });
  server.create("access-level", {
    slug: "controlling",
    requiredGrantType: "USER",
  });
  server.create("access-level", {
    slug: "token",
    requiredGrantType: "TOKEN",
  });
  server.create("access-level", {
    slug: "registered-user",
    requiredGrantType: "AUTHENTICATED-PUBLIC",
  });
  server.create("access-level", {
    slug: "public-access",
    requiredGrantType: "ANONYMOUS-PUBLIC",
  });

  server.createList("user-group", 5).forEach((userGroup) => {
    server
      .createList("user", 2, { defaultGroup: userGroup })
      .forEach((user) => {
        server.create("instance-acl", { user });
      });
  });
}
