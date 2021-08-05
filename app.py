""" 
*imports*
"""
from flask import Flask,render_template, request
import numpy as np
import pandas as pd
""" 
*initial declarations*
"""
app = Flask(__name__, template_folder='Templates', static_folder='static')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

""" 
!!Linear regression logic
"""
def linear_regression(x,y):
    data = pd.DataFrame()
    data["x"]=x
    data["y"]=y
    X_mean = np.mean(x)
    y_mean =np.mean(y)
    diffx= x-X_mean
    diffy = y-y_mean
    data["(x-x̄)"]=diffx
    data["(y-ȳ)"]=diffy
    sqdiffx = (x-X_mean)**2
    data["(x-x̄)²"] = sqdiffx
    data["(x-x̄)*(y-ȳ)"]=(x-X_mean)*(y-y_mean)
    m=np.sum(data["(x-x̄)*(y-ȳ)"])/np.sum(data["(x-x̄)²"])
    c=y_mean-m*X_mean
    yp = m*x + c #datapoints of the line to be plotted
    data["ŷ"] = yp
    data["y-ŷ "] = y-yp
    data["ŷ-ȳ"] = yp-y_mean
    data["(y-ȳ)²"] = (y-y_mean)**2
    data["(ŷ-ȳ)²"] = (yp-y_mean)**2
    least_square = np.sum(data["(ŷ-ȳ)²"])/np.sum(data["(y-ȳ)²"])
    bfl = {"m":m,"c":c}

    return least_square,bfl,yp

""" 
!prepares data for plotting purposes:
    !data : {x,y}
    !bfl : {x,yp}
"""
def data(x,y,yp):
    data = []
    for i,j in zip(x,y):
        data.append({"x":i,"y":j})
    bfl_data = []
    for k,l in zip(x,yp):
        bfl_data.append({"x":k,"y":l})
    return data,bfl_data
""" 
! calculates the estimated value of y from yp = mx+c
! bfl = {"m":m, "c": c}
 """
def predict_4x(predict_x,bfl):
    predict_y = bfl["m"]*predict_x + bfl["c"]
    return predict_y


# @app.route('/',methods=[ 'POST','GET'])
# def index():
#     try:
#         if request.method == 'POST':
#             flag = True 
#              = False
#             i1 = (request.form['x'])
#             i2 = (request.form['y'])
#             x = []
#             for each in i1.split(','):
#                 x.append(float(each))
#             y = []
#             for each in i2.split(','):
#                 y.append(float(each))
#             x = np.array(x,dtype=np.float32)
#             y = np.array(y,dtype=np.float32)
#             least_square,table,bfl,yp = linear_regression(x,y)
#             d,bfl_data = data(list(x),list(y),list(yp))
#             print("check2")
#             if(request.form["predict_4x"]!=""):
#                 print("check3")
#                 pred_flag = True
#                 predict_x = float(request.form["predict_4x"])
#                 predict_y = predict_4x(predict_x,bfl)
#                 return render_template("index.html", =  ,x=list(x),y=list(y),least_square = least_square,table = [table],bfl=bfl,flag=flag,data=d, bfl_data = bfl_data,i1=i1,i2=i2,predict_x = predict_x, predict_y = predict_y, pred_flag = pred_flag)
#             else:
#                 pred_flag = False
#                 return render_template("index.html", =  ,x=list(x),y=list(y),least_square = least_square,table = [table],bfl=bfl,flag=flag,data=d, bfl_data = bfl_data,i1=i1,i2=i2, pred_flag = pred_flag)
#         else:
#             flag = False
#             return render_template("index.html",flag=flag, = True)
#     except:
#         return render_template("error.html")

""" 
handle zeros
 """
def handle_zeros(CGPA):
    knwn_cgpa = []
    for i in range(1,len(CGPA)):
        if(CGPA[i]!=0 and CGPA[i-1]==0):
            return -1
        elif(CGPA[i-1]==0):
           return (knwn_cgpa[:i-1])
        knwn_cgpa.append(CGPA[i-1])
def sem_i_sampled(knwn_cgpa):
    # knwn_sems = np.arange(1,len(knwn_cgpa)+1)
    sem_i_sampled = []

    for i in range(1,len(knwn_cgpa)+1):
        sem_i_sampled.append(i)
    sem_i_sampled = np.array(sem_i_sampled,np.int32)
    return sem_i_sampled



def cgpa_i_sampled(knwn_cgpa):
    i_sampled_CGPA = list(knwn_cgpa)
    for _ in range(len(knwn_cgpa)):
        i_sampled_CGPA = np.append(i_sampled_CGPA,list(knwn_cgpa))
    return i_sampled_CGPA
""" 
!landing page
 """
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        sems = ["sem1","sem2","sem3","sem4","sem5","sem6","sem7",]
        CGPA = []
        for sem in sems:
            """ 
            !assertionError(int(request.form[str(sem)])>10)
             """
            CGPA.append(request.form[str(sem)])
        
        CGPA = np.array(CGPA,np.float32)

        knwn_cgpa = handle_zeros(CGPA)
        unknwn_cgpa = np.array([],np.float32)
        
        sem_knwn = [x for x in range(1,len(knwn_cgpa)+1)]
        sem_unknwn =[x for x in range(len(sem_knwn)+1,9)]
       
        """ 
        !if knwn_cgpa == [] or knwn_cgpa == -1 
        !                           or knwn_cgpa >10:
            !throw error(assertion errors)
         """


        """
            *i times sampled knwn cgpa's 
        """
        cgpa_i_sampled_res = cgpa_i_sampled(knwn_cgpa)
        sem_i_sampled_res = sem_i_sampled(cgpa_i_sampled_res) 
        """ 
        *use linear regression
         """
        least_square,bfl,yp = linear_regression(sem_i_sampled_res,cgpa_i_sampled_res)
        
        """ 
        *predict for last j sems
         """
        predictions = []
        for sem in sem_unknwn:
            predictions.append(predict_4x(sem,bfl))
        print(sem_i_sampled_res)
        print(predictions)
        















        return render_template("results.html")
    else:
        return render_template("index.html")

@app.route('/feedback')
def feedback():
    return render_template("feedback.html")









if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)