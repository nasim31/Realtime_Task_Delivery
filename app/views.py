from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import json
import os
import psycopg2
from django.http import JsonResponse
from psycopg2.extras import RealDictCursor

engine = psycopg2.connect(
    database="akshatProject",
    user="akshat",
    password="akshat1234",
    host="project.c55dan5ybmd7.us-east-1.rds.amazonaws.com",
    port='5432'
)

# Create your views here.

def login(request):
    return render(request,'Login.html')

def manager(request,username):
    return render(request,'StoreManager.html',{"Username":username})

def delivery(request,username):
    return render(request,'Delivery.html',{"Username":username})

def index(request):
    return render(request, 'index.html', {})

def room(request, room_name='lobby'):
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def getmytasksquota(request,username):
    cur = engine.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from task where task_status = 'Accepted' and acceptedby = '"+username+"'; ")
    res = cur.fetchall()
    cur.close()
    return JsonResponse(len(res),safe=False)



def getNextTask(request):
    cur = engine.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from task where task_status = 'New' order by priority desc limit 1; ")
    res = cur.fetchall()
    cur.close()
    if(len(res)>0):
        return JsonResponse(res[0])
    else:
        return JsonResponse({})
    # return HttpResponse('<h1>Welcome '+username+' '+str(res)+' '+"select * from users where username = '"+username+"' LIMIT 1 "+'</h1>')
def getMyTaks(request,username):
    cur = engine.cursor(cursor_factory=RealDictCursor)
    cur.execute("select usrtype from users where username = '"+username+"' ")
    res = cur.fetchall()
    

    if(res[0]['usrtype']=='Manager'):
        cur.execute("select * from task where createdby = '"+username+"' order by priority ")
        res = cur.fetchall()
        cur.close()
        return JsonResponse(res, safe=False)    
    elif (res[0]['usrtype']=='Delivery'):
        cur.execute("select * from task where acceptedby = '"+username+"'  order by priority")
        res = cur.fetchall()
        cur.close()
        return JsonResponse(res, safe=False)    
    return JsonResponse({})

def deleteTask(request):
    if request.method == "POST":
        res = json.loads(request.body.decode("utf-8"))
        cur = engine.cursor()
        cur.execute("update task set task_status = 'Cancelled' where title= '"+str(res['TaskId'])+"'   ")
        engine.commit()
        cur.close()
        return JsonResponse({"Status":"DONE"},safe=False)
    else:
        return JsonResponse({})

def loginApi(request):
    if request.method == "POST":
        res = json.loads(request.body.decode("utf-8"))
        cur = engine.cursor(cursor_factory=RealDictCursor)
        cur.execute("select usrtype from users where username = '"+res['username']+"' and pass ='"+res['Password']+"' limit 1 ")
        result = cur.fetchall()
        cur.close()
        if(len(result)>0):
            print(result[0])
            newresult = json.loads(json.dumps(result[0]))
            
            typeOfUser = newresult["usrtype"]
            if(typeOfUser == 'Manager'):
                url = 'http://3.83.129.144:8000/manager/'+res['username']+'/'
                return JsonResponse({"url":url},safe=False)
            else:
                url = 'http://3.83.129.144:8000/delivery/'+res['username']+'/'
                return JsonResponse({"url":url},safe=False)
        else:
            return JsonResponse({})
    else:
        return JsonResponse({})
