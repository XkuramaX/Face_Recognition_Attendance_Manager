const express = require("express");
const app = express.Router();

const routes = require("./routes/index")

const exp = express()

exp.set("view engine", "ejs");


app.get("/home", (req,resp) => {
    resp.render('home.ejs')
})

exp.use("/abcd", app)
exp.use("/welcome", routes);


exp.listen(3000, ()=> {
    console.log('The server is working')
})

module.exports = app

