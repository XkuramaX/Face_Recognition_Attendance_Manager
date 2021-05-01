const express = require("express");
const app = express();

const requireLogin = require('../middlewares/required_login')

const teacher = require("./login/teacher")
const student = require("./login/student")
const register = require("./login/registration")
const contact = require("./login/contact")




app.use("/teacher", teacher)
app.use("/student", student)
app.use("/registration", requireLogin, register)
app.use("/contact", contact)

app.get('/home', (req,resp) => {
    console.log("Session: ",req.session)
    console.log('app is running')
    resp.render("welcome.ejs")
})

module.exports = app