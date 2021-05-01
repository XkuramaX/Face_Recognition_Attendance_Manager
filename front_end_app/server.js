const express = require("express");
const session = require('express-session')
const bodyParser = require("body-parser");
const app = express();
app.use(session({
    secret : "123456",
    resave : false,
    saveUninitialized : false,
    cookie : {
        httpOnly : true,
        secure : false,  //for http, in case if https it should be true
        maxAge : null
    }
}))

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const routes = require("./routes/index")



app.set("view engine", "ejs");

app.use(express.static('assets'));

app.get("/home", (req,resp) => {
    resp.render('home.ejs')
})

app.use("/", routes);


app.listen(3000, ()=> {
    console.log('The server is working')
})