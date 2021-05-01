module.exports = async function required_login(req,res,next) {
    const token = req.session.token;
    if (token) {
        next()
    } else {
        res.render("error.ejs", { error : "Unauthorized!" })
    }
}