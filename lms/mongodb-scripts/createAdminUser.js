db = db.getSiblingDB("admin");
db.createUser({
    user: "admin",
    pwd: "securePassword",
    roles: [{ role: "root", db: "admin" }]
});