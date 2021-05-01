const express = require("express");
const app = express.Router();
const fetch = require('node-fetch')

app.get("/", async (req, resp) => {
    let users = await fetch("http://localhost:5555/users/list",{method:"GET", headers:{"Content-type":"application/json; charset=UTF-8", "Authorization": "Bearer "+req.session.token}, mode:"cors", credentials:"include"})
    users = await users.json()
    console.log(users)
    resp.render("Contact.ejs")
    })


module.exports = app