const express = require("express");
const app = express.Router();

app.get("/", (req, resp) => {
    resp.render("Registration.ejs")
    })


module.exports = app