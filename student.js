const express = require("express");
const app = express.Router();

app.get("/", (req, resp) => {
    resp.render("Student_Login.ejs")
    })


module.exports = app