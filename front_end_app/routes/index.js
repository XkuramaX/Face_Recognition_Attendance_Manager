const express = require("express");
const app = express.Router();


const home = require("./home/home")
const teacher = require("./login/teacher")
const student = require("./login/student")
const register = require("./login/registration")
const contact = require("./login/contact")



app.use("/", home)
app.use("/teacherlogin", teacher)
app.use("/studentlogin", student)
app.use("/registration", register)
app.use("/contact", contact)

app.get('/home', (req,resp) => {
    console.log('app is running')
    resp.render("welcome.ejs")
})

module.exports = app