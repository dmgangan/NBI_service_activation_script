def regist():
    if request.method == "POST":
        with sql.connect("database.db") as con:
            cur = con.cursor()
            try:
                # ... Collecting form info ...

                cur.execute("SELECT * FROM users WHERE name = ?", (username))

                if cur.fetchone() is not None:
                    flash("That username is already taken...")
                    return render_template('register.html')
                else:
                    cur.execute("INSERT INTO users (name,password,email) VALUES (?,?,?)",(username,passwordencr,email) )
                    con.commit()
                    flash (...)
             except:
                 con.rollback()

             finally:
                 session['logged_in'] = True
                 session['username'] = username
                 # ... mailing code ...
