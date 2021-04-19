const express = require("express");
const app = express.Router();

app.get("/", (req, resp) => {
    /*let name = "debasmita"
    let arr = ["debasmita", "akash", "poulami"]*/
    resp.render("Teacher_Login.ejs")
    })


module.exports = app