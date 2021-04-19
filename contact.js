const express = require("express");
const app = express.Router();

app.get("/", (req, resp) => {
    resp.render("Contact.ejs")
    })


module.exports = app