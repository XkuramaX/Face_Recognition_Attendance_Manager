const express = require("express");
const app = express();

const routes = require("./routes/index")


app.set("view engine", "ejs");

app.use("/", routes);

app.listen(3030, ()=> {
    console.log('The server is working')
})


