const express = require("express");
let fetch = require("node-fetch")
let requireLogin = require('../../middlewares/required_login')

const app = express();


app.get("/", (req, resp) => {
    resp.render("Student_Login.ejs")
    })

app.post("/login",async(req, resp) => {
    try {
        let response = await fetch("http://localhost:5555/login",{method:"POST", body:JSON.stringify(req.body), headers:{"Content-type":"application/json; charset=UTF-8"}, mode:"cors", credentials:"include"})
        response = await response.json()
        console.log(response)
        if( response.success == true ){
            req.session.token = response.token
            resp.redirect("/contact")
        } else {
            resp.redirect("/login")
        }
    } catch (error) {
        console.log(error)
    }
})

// app.get("/profile", async (req,res) => {
//     try{


//     } catch ( error ) {

//     }
// })


module.exports = app