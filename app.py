from flask import Flask,render_template,redirect,request,flash,url_for
import sqlite3 as sql
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
@app.route('/')
def index():
    return render_template("base.html")

@app.route('/cr')
def hello():
    return render_template('createpage.html')

@app.route('/cr',methods=['GET','POST'])
def invers():
    if request.method=="POST":

        id=request.form.get('id')
        name=request.form.get('name')
        email=request.form.get('email')
        quntity=request.form.get('qun')
        gender=request.form['gender']
        type=request.form['group']
        date=datetime.date.today()
        date=date.strftime("%Y-%m-%d")
        print(id,name,quntity,type,gender,email,date)
        con=sql.connect("/home/hacker/Desktop/task/task.db")
        cur=con.cursor()
        try:
            cur.execute("insert into milk values(?,?,?,?,?,?,?)",(id,name,email,gender,quntity,type,date))
            flash('one record insered ','info')
            con.commit()
            con.close()

        except Exception as e:
            print(e)
            flash('insert  record erorr ','info')

        return redirect(url_for("ditails"))
    

@app.route('/datalist')
def ditails():
        con=sql.connect("/home/hacker/Desktop/task/task.db")
        cur=con.cursor()
        cur.execute("select * from milk")
        data=cur.fetchall()
        print(data)
        return render_template("datalist.html",provider=data)

@app.route('/datalist',methods=['POST'])
def ditail():
    if request.method=="POST":        
        date=request.form.get('date')
        con=sql.connect("/home/hacker/Desktop/task/task.db")
        cur=con.cursor()
        cur.execute("select * from milk where date=?",(date,))
        data=cur.fetchall()
        print(data)
        return render_template("datalist.html",provider=data)

@app.route("/<int:id>/delete")
def delete(id):
    

    return render_template("delete.html",id=id)
    
    
@app.route("/delete",methods=["POST"])
def delet():
    if request.method=="POST":
        id=request.form.get('id')
        con=sql.connect("/home/hacker/Desktop/task/task.db")
        cur=con.cursor()
        cur.execute("delete from milk where id=?",(id,))
        con.commit()
        con.close()
        flash("record deleted successfully")


    return redirect(url_for("ditails"))

@app.route("/<int:id>/update")
def update(id):
    con=sql.connect("/home/hacker/Desktop/task/task.db")
    cur=con.cursor()
    cur.execute("select * from milk where id=?",(id,))
    data=cur.fetchone()
    print(data)
    

    return render_template("update.html",data=data)     

@app.route("/update",methods=['POST'])
def updat():
    
    if request.method=="POST":

        id=request.form.get('id')
        name=request.form.get('name')
        email=request.form.get('email')
        quntity=request.form.get('qun')
        gender=request.form['gender']
        type=request.form['group']
        print(id,name,quntity,type,gender,email)
        con=sql.connect("/home/hacker/Desktop/task/task.db")
        cur=con.cursor()
        try:
            cur.execute("update  milk set name=?,email= ?,gender=?, qun=?,type=? where id=?",(name,email,gender,quntity,type,id))
            flash('updated success','info')
            con.commit()
            con.close()

        except Exception as e:
            print(e)
            flash('insert  record erorr ','info')

        return redirect(url_for("ditails"))

if __name__ == '__main__':
    app.run(debug=True)
