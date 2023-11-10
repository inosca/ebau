import { faker } from "@faker-js/faker";

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
    requiredGrantType: "service",
  });
  server.create("access-level", {
    slug: "controlling",
    requiredGrantType: "user",
  });
  server.create("access-level", {
    slug: "token",
    requiredGrantType: "token",
  });
  server.create("access-level", {
    slug: "registered-user",
    requiredGrantType: "authenticated-public",
  });
  server.create("access-level", {
    slug: "public-access",
    requiredGrantType: "anonymous-public",
  });

  server.createList("user-group", 5).forEach((userGroup) => {
    server
      .createList("user", 2, { defaultGroup: userGroup })
      .forEach((user) => {
        server.create("instance-acl", { user });
      });
  });
}
