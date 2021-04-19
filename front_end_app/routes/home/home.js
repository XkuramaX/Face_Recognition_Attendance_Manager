const express = require("express");
const app = express.Router();

// Route for home page
app.get("/", (req, resp) => {
    resp.render("Home.ejs")
})


module.exports = app