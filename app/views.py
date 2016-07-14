from app import app
from flask import render_template
from flask import request
import os, json
import MySQLdb
from flask import Flask, session, redirect, url_for
from collections import OrderedDict
import random

PATH_TO_DATA = os.getcwd()+'/app/static/data'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

num_patients = 0
patient_id_single_page = 1

@app.route('/sortPatients/',methods=['POST'])
def sortPatients():
    sortBy = request.form['sortBy']


    patient_image = []
    patient_image = session['patient_image']

    print patient_image
    print '\n'
    btemp = []
    for i in patient_image:
        btemp.append(int(i[2]))

    if int(sortBy) == 1:
        patient_image = sorted(patient_image, key=lambda tup: tup[2])
    elif int(sortBy) == 2:
        patient_image = sorted(patient_image, key=lambda tup: tup[3])
    else:
        patient_image = sorted(patient_image, key=lambda tup: tup[4])

    atemp = []
    for i in patient_image:
        atemp.append(int(i[2]))

    print btemp, atemp
    diffCount = sum(i != j for i, j in zip(btemp, atemp))
    if diffCount == 0:
        if int(sortBy) == 1:
            patient_image = sorted(patient_image, key=lambda tup: tup[2],reverse=True)
        elif int(sortBy) == 2:
            patient_image = sorted(patient_image, key=lambda tup: tup[3],reverse=True)
        else:
            patient_image = sorted(patient_image, key=lambda tup: tup[4],reverse=True)

    print "After $$$$$$$$$"
    print patient_image
    print '\n'

    temp_summary = dict(session['patient_summary'])
    patient_summary = {}
    for key, value in temp_summary.iteritems():
        patient_summary[int(key)] = value
    print patient_summary
    print '\n'
    print patient_summary
    print '\n'

    session['patient_image'] = patient_image
    session['patient_summary'] = patient_summary

    return render_template('choosePatient.html', patient_image=patient_image,
        patient_summary=patient_summary)

@app.route('/')
def index():
    patient_image = []
    patient_summary = {}
    id = 1
    los = 0
    bedNo = 0
    patients = os.listdir(PATH_TO_DATA)
    for patient in patients:
        los = random.randrange(1,3)
        bedNo = random.randrange(100,300)
        print los
        patient_image.append( ('../static/data/'+patient+'/image.png', patient,id,los,bedNo) )
        id+=1

    db = MySQLdb.connect("52.33.170.186","hciuser","hciproject","hci" )
    cursor = db.cursor()
    cursor.execute("SELECT id, summary from patients");
    data = cursor.fetchall()

    for row in data:
        patient_summary[row[0]] = row[1]

    db.close()

    session['patient_image'] = patient_image
    session['patient_summary'] = patient_summary
    print '\n'
    print patient_summary
    print '\n'
    return render_template('choosePatient.html', patient_image=patient_image,
        patient_summary=patient_summary)


@app.route('/bfilters/',methods=['GET'])
def vitalsGet():
    plist = [session['onepp'], session['twopp']] if session['num_ids']==2 else [session['onepp']]
    patient_image = []
    for patient in plist:
        patient_image.append(('../'+patient))
    return render_template('chooseOptions.html', patient_image=patient_image)

@app.route('/bfilters/',methods=['POST'])
def vitals():
    global patient_id_single_page, num_patients

    if request.method == 'POST':
        plist = request.form['pids']
        print plist
        plist = plist.split(',')
        num_patients = request.form['alignment']
        alignment = request.form['alignment']
        alignment = alignment.split(",")
        print num_patients
        num_patients = len(num_patients.split(","))
        if num_patients == 1:
            patient_id_single_page = int(request.form['alignment'])
            session['onepp']= request.form['pids']
            session['num_ids'] = 1
        else:
            session['multiple_ids'] = (alignment[0],alignment[1])
            session['onepp'] = plist[0]
            session['twopp'] = plist[1]
            session['num_ids'] = 2
    patient_image = []
    for patient in plist:
        patient_image.append(('../'+patient))
    return render_template('chooseOptions.html', patient_image=patient_image)

@app.route('/showVitals', methods=['POST'])
def showVitals():
    body_system = request.form.getlist("bodySystem")
    if body_system == []:
        body_system = session['tmp']
        vitals_list = []
        vitals_list = request.form.getlist("vitals")
    else:
        session['tmp'] = body_system
        vitals_list = ['1','2','3','4','5','6']

    global num_patients

    if num_patients > 1:
        ppath1 = session['onepp']
        ppath2 = session['twopp']

        pname1 = ppath1.split('/')[3]
        pname2 = ppath2.split('/')[3]

        patient_id = session['multiple_ids'][0]

        plan_results1 = {}

        db = MySQLdb.connect("52.33.170.186","hciuser","hciproject","hci" )
        cursor = db.cursor()
        cursor.execute("SELECT body_system,plan1 from body_systems where patient_id="+ str(patient_id))
        data = cursor.fetchall()

        for row in data:
            plan_results1[row[0]] = row[1].split('^')

        # disconnect from server
        db.close()

        patient_id = session['multiple_ids'][1]

        plan_results2 = {}

        db = MySQLdb.connect("52.33.170.186","hciuser","hciproject","hci" )
        cursor = db.cursor()
        cursor.execute("SELECT body_system,plan1 from body_systems where patient_id="+ str(patient_id))
        data = cursor.fetchall()

        for row in data:
            plan_results2[row[0]] = row[1].split('^')

        # disconnect from server
        db.close()

        return render_template('show_two.html', body_system = body_system,
                               ppath1 = ppath1, ppath2=ppath2,pname1=pname1,pname2=pname2,
                               plan_results1 = plan_results1,plan_results2 = plan_results2)
    else:
        global patient_id_single_page
        # fetch value for resident plan
        patient_id = patient_id_single_page

        plan_results = {}

        db = MySQLdb.connect("52.33.170.186","hciuser","hciproject","hci" )
        cursor = db.cursor()
        cursor.execute("SELECT body_system,plan1 from body_systems where patient_id="+ str(patient_id))
        data = cursor.fetchall()

        for row in data:
            plan_results[row[0]] = row[1].split('^')

        # disconnect from server
        db.close()

        ppath = session['onepp']
        print '########',ppath
        return render_template('index.html', body_system = body_system, vitals_list = vitals_list,
            plan_results = plan_results,ppath = ppath, pname=ppath.split("/")[3])

@app.route('/updateResidentPlan',methods=['POST'])
def updateResidentPlan():

    global patient_id_single_page

    new_plan = request.form['residentplan']
    body_system = request.form['body_system']
    new_plan = '^'.join(new_plan.split("\n"))

    db = MySQLdb.connect("52.33.170.186","hciuser","hciproject","hci" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    q = "UPDATE body_systems set plan1='%s' WHERE body_system='%s' AND patient_id='%s'" % (
        new_plan, body_system, patient_id_single_page)
    cursor.execute(q)
    db.commit()

    # disconnect from server
    db.close()

    return json.dumps({'status':'OK'})

@app.route('/updateResidentPlanTwo',methods=['POST'])
def updateResidentPlanTwo():

    id1, id2 = session['multiple_ids'][0], session['multiple_ids'][1]

    new_plan = request.form['residentplan']
    body_system = request.form['body_system']
    patientNum = request.form['patientNum']
    new_plan = '^'.join(new_plan.split("\n"))

    patient_id = id1 if patientNum == '1' else id2

    db = MySQLdb.connect("52.33.170.186","hciuser","hciproject","hci" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    q = "UPDATE body_systems set plan1='%s' WHERE body_system='%s' AND patient_id='%s'" % (
        new_plan, body_system, patient_id)
    print "Query: %s " %(q)
    cursor.execute(q)
    db.commit()

    # disconnect from server
    db.close()

    return json.dumps({'status':'OK'})

@app.route('/createSummary',methods=['POST'])
def createSummary():
    global patient_id_single_page

    db = MySQLdb.connect("52.33.170.186","hciuser","hciproject","hci" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    q = "UPDATE patients set summary=NOW() WHERE id='%s'" % (
        patient_id_single_page)
    cursor.execute(q)
    db.commit()

    # disconnect from server
    db.close()

    return redirect(url_for('index'))

@app.route('/createsummary',methods=['POST'])
def createsummary():
    pid = int(request.form['patient_id'])

    db = MySQLdb.connect("52.33.170.186","hciuser","hciproject","hci" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    q = "UPDATE patients set summary=NOW() WHERE id='%s'" % (
        session['multiple_ids'][pid])
    print 'patient ID is : '+str(session['multiple_ids'][pid])
    cursor.execute(q)
    db.commit()

    # disconnect from server
    db.close()

    return redirect(url_for('index'))

@app.route('/quickView',methods=['POST'])
def quickView():
    return render_template('quickView.html')