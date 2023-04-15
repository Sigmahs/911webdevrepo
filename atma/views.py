from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth import get_user
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt

from PIL import Image

import json
import ipmd_app.settings as sett
import datetime
import json
import operator
import boto3
import io
#import sagemaker #ask Erik

import glob
import os
import re
from shutil import rmtree

from atma.models import Document, PictureSubmission, VideoSubmission, Thread, Comment, PictureUser, VideoUser
from atma.forms import DocumentForm, ThreadForm, CommentForm, UserVideoForm


from tempfile import TemporaryFile
from django.contrib.auth.decorators import login_required

def save_img(image_bytes, object_name):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_client = boto3.client('s3', region_name='us-east-2',
                             aws_access_key_id='AKIAQFEAV2W63TXCMCH3',
                             aws_secret_access_key= "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")
    try:
        out_img = io.BytesIO(image_bytes)
        s3_client.upload_fileobj(out_img,'atma-website-storage', object_name)

        print("upload succeed!")
    except:
        return False
    return True

#TO DO: replace the rekognition function with SageMaker, like the one from 911


def get_aws_prediction(content):

    client = boto3.client('runtime.sagemaker')
    #client = boto3.client('sagemaker', region_name='us-east-2',
                                 #aws_access_key_id="AKIATIGBJSAAQH6C3RHY",
                                 #aws_secret_access_key="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")
    boto_session = boto3.Session(region_name = "us-east-2")
    sess = sagemaker.Session(boto_session = boto_session, sagemaker_client=client)
    endpoint_name = "911ATMA-20201026"
    deployed_endpoint = sagemaker.predictor.RealTimePredictor(endpoint_name, sagemaker_session = sess)
    content = Image.open(io.BytesIO(content)) #changing input from bittype to image
    new_image = content.resize((224, 224))
    print("new image create", new_image)
    payload = io.BytesIO()
    new_image.save(payload, format='PNG')
    payload = payload.getvalue()
    print("payload value")
    print("payload")
    print(payload)
    print(len(payload))
    #ask daniel
    response = client.invoke_endpoint(EndpointName=endpoint_name,
                                      Body=json.dumps(payload))
    response_body = response['Body']
    print(response_body.read())
    #deployed_endpoint.content_type = "application/x-image"
    #results = json.loads(deployed_endpoint.predict(payload))
    classes = ["Crime", "Crime Alert", "No Action", "Emergency", "Medical", "Medical Alert", "No Emergency"]
    dictionary = {}

    for i in range(len(classes)):
        curr_class = classes[i]
        result = results[i]
        dictionary[curr_class] = result

    dictionary = {k: v for k, v in sorted(dictionary.items(), key = lambda item: item[1], reverse = True)}
    print(dictionary)

    return dictionary

def show_softmax_result(data):

    z_exp = [1/(1-i) - 1 for i in data]
    sum_z_exp = sum(z_exp)
    return [i / sum_z_exp for i in z_exp]

#aws_access_key_id='AKIATIGBJSAAQH6C3RHY',
                                 #aws_secret_access_key= "l/7Bn7h37zDyK67UtlzdHPpJ/gBbHYSUrhNtclNI"
    # Create your views here.
@login_required
def home(request):
    subs = 0
    user = request.user
    date = datetime.date.today()
    date = str(date.year)+str(date.month) + str(date.day)+"_"
    """try:
        if user.pictureuser.LastDateUsed == datetime.date.today():
            subs = user.pictureuser.TimesUsedToday
    except:
        pass"""
    firstTime = True
    if not PictureUser.objects.filter(User=user).exists():
        pic_user = PictureUser(User=user,LastDateUsed=datetime.date.today(),TimesUsedToday=0)
        pic_user.save()
    pic_user = PictureUser.objects.get(User=user)
    subs = 0
    if pic_user.LastDateUsed == datetime.date.today():
        subs = pic_user.TimesUsedToday
        firstTime = True

    if user.is_active:
        return render(request, 'atma/home.html', {"firstTime": firstTime})
    else:
        return redirect("/accounts/confirm-email")

@xframe_options_exempt
def results(request):
    return render(request, 'atma/results.html')


def video(request):
    return render(request, 'atma/video.html')


@csrf_exempt
@login_required
def submit(request):
    subs = 0
    user = request.user
    date = datetime.date.today()
    date = str(date.year)+str(date.month) + str(date.day)+"_"
    """try:
        if user.pictureuser.LastDateUsed == datetime.date.today():
            subs = user.pictureuser.TimesUsedToday
    except:
        pass"""

    if not PictureUser.objects.filter(User=user).exists():
        pic_user = PictureUser(User=user,LastDateUsed=datetime.date.today(),TimesUsedToday=0)
        pic_user.save()
    pic_user = PictureUser.objects.get(User=user)
    subs = 0
    if pic_user.LastDateUsed == datetime.date.today():
        subs = pic_user.TimesUsedToday
    else:
        pic_user.TimesUsedToday = 0
    pic_user.LastDateUsed = datetime.date.today()
    pic_user.TimesUsedToday +=1
    pic_user.save()
    if subs >= 5 and not (user.is_superuser):
        return render(request,'atma/fail2.html')


    if request.method == 'POST' :
        repeat = request.POST['repeat']
        avatar = request.FILES['avatar']

        fs = FileSystemStorage()
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            pass

    labels = ['Anger', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Neutrality', 'Sadness', 'Surprise']

    image_name = date + user.username + "_"+str(subs) + '.png'
    avatar = avatar.read()
    print("type", type(avatar))
    print("test")
    #change this line

    #MUST CHANGE get_aws_prediction function with new function
    save_img(avatar, image_name)
    results_911 = get_aws_prediction(avatar)
    print(results_911)

    results = ""
    posted = {}
    mood = {}
    labels = []
    scores = []
    bar_labels = []
    bar_scores = []
    mood_labels = []
    mood_scores = []
    # need to change to emotion colors
    emotion_colors = {"Anger":"#DC1E41", "Contempt":"#F2766B",
    "Disgust":"#7E476F", "Fear":"#134F72", "Neutral":"#B9B6B2", "Happy":"#66E898",
    "Sad":"#393551", "Surprise":"#EE93E1"}
    pie_colors = []
    bar_colors = []


    for i in emotion_response["CustomLabels"]:
        labels.append(i["Name"])
        scores.append(float(i["Confidence"])/100.0)

    for i in mood_response["CustomLabels"]:
        mood_labels.append(i["Name"])
        mood_scores.append(float(i["Confidence"])/100.0)
        mood[i["Name"]] = float(i["Confidence"])/100.0

    # emotion from highest to lowest
    pre_scores, pre_labels = (list(t) for t in zip(*sorted(zip(scores, labels), reverse = True)))

    # emotion from lowest to higest
    scores, labels  = (list(t) for t in zip(*sorted(zip(scores, labels), reverse = True)))

    for i in range(len(scores)):
        if scores[i] > 0.25:
            bar_labels.append(labels[i])
            bar_scores.append(scores[i])

    # softmax_scores = show_softmax_result(scores)
    # Rekognition model has default feature of softmax, remove this for now

    highest_mood = max(mood.items(), key=operator.itemgetter(1))[0]
    if highest_mood == "Nu":
        mood_color  = "#B4B1B1"
        final_mood = "Neutral"
    elif highest_mood == "Po":
        mood_color  = "#92CF75"
        final_mood = "Positive"
    else:
        mood_color  = "#FB6C6C"
        final_mood = "Negative"

    bar_scores = [round (input  , 2) for input in bar_scores]
    #softmax_scores = [round (input , 2) for input in softmax_scores]  remove softmax for now

    #create in text for pie chart with scores bigger than 10
    appropriate_texts = []
    for i in pre_scores:
        if i >= 0.10:
            appropriate_texts.append(i)
        else:
            appropriate_texts.append(0)
    # appropriate_texts = json.dumps(appropriate_texts)
    appropriate_texts = [str(round(i*100,1)) + "%" for i in appropriate_texts if i >0]

    # create appropriate colors for bar and pie charts
    for i in pre_labels:
        pie_colors.append(emotion_colors[i])
    for i in bar_labels:
        bar_colors.append(emotion_colors[i])

    # set bar width depending on the number of bar scores greater than 0.15
    if len(bar_scores) == 1:
        bar_widths = 0.28
    elif len(bar_scores) == 2:
        bar_widths = [0.55 for i in range(len(bar_scores))]
    elif len(bar_scores) == 3:
        bar_widths = [0.8 for i in range(len(bar_scores))]
    elif len(bar_scores) == 4:
        bar_widths = [0.95 for i in range(len(bar_scores))]
    elif len(bar_scores) == 5:
        bar_widths = [0.95 for i in range(len(bar_scores))]
    elif len(bar_scores) == 6:
        bar_widths = [0.95 for i in range(len(bar_scores))]

    #edit this based on new prediction function
    posted["success"] = 1
    posted["labels"] = labels
    posted["scores"] = scores
    posted["softmax_scores"] = pre_scores
    posted["bar_labels"] = bar_labels
    posted["bar_scores"] = bar_scores
    posted["mood_scores"] = mood_scores
    posted["mood_labels"] = mood_labels
    posted["final_mood"] = final_mood
    posted["final_mood_score"] = str(round(max(mood_scores),3) * 100) + "%"
    posted["bar_widths"] = bar_widths
    posted["mood_color"] = mood_color
    posted["pie_labels"] = pre_labels
    posted["pie_colors"] = pie_colors
    posted["appropriate_texts"] = appropriate_texts
    posted["bar_colors"] = bar_colors
    posted["911"] = {"Crime": 0.07142857, "Crime Alert": 0.07142857, "No Action": 0.07142857, "Emergency": 0.5714285714, "Medical":0.07142857, "Medical Alert":0.07142857, "No Emergency":0.07142857}

    if scores == [] :
        posted["success"] = 0
    return render(request,'atma/results.html' ,{"posted":posted});

@csrf_exempt
def faceTracker(request):
    if request.method == 'POST' :
        repeat = request.POST['repeat']
        avatar = request.FILES['avatar']
    else:
        return render(request,'atma/video.html');


    left, up, width, height = image_shown_tracker(avatar.file.getvalue(), repeat)
    return render(request, 'atma/overlay.html',{'left':left,'up':up,'width':width,'height':height})



def overlay(request):
    return render(request, 'atma/overlay.html');

def results_overlay(request):
    return render(request, 'atma/results_overlay.html');


import sys




# 'content' is base-64-encoded image data.
def get_prediction(content, project_id, model_id):
  prediction_client = automl_v1beta1.PredictionServiceClient()

  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'image': {'image_bytes': content }}
  params =  { "score_threshold": "0" }
  request = prediction_client.predict(name, payload, params)
  return request

@csrf_exempt
def videosubmit(request):

    if request.POST['limit_reached'] == 'true' :
        return render(request, 'atma/fail2.html')

    if request.method == 'POST' and request.POST['end'] == 'false':
        repeat = request.POST['repeat']
        avatar = request.FILES['avatar']
        fs = FileSystemStorage()
        form = DocumentForm(request.POST, request.FILES)
    else:
        username = get_user(request)
        submission = VideoSubmission(User=username,Date=datetime.date.today())
        submission.save()
        return render(request,'atma/fail2.html')

# Convert_Single_Img
    try:
        #print (uploaded_file_url)
        # Currently only test the first face in the image. Will add feature later on
        faces = []
        test_img_data = convert_single_img(avatar.file.getvalue())[0] #remove one [0] and should replace by a for loop
        for i in test_img_data:
            faces.append(i.reshape(200,200))
    except:
        return render(request,'atma/fail.html')

    all_data = []
    for each_face in faces:
        push_data = []
        each_face = each_face/255
        for i in each_face:
            row = []
            for j in i:
                row.append([j])
            push_data.append(row)
        all_data.append(push_data)

    try:
        posted={}
        labels = ['Anger', 'Contempt', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
        for i in range(0, len(all_data)):
            # convert data into json
            data = {"instances":[all_data[i]]}
            push_data_json = json.dumps(data, sort_keys=True, separators=(',', ': '))
            r1 = requests.post("http://35.224.178.33:8501/v1/models/model1:predict", data=push_data_json)
            prediction_1 = json.loads(r1.text)['predictions'][0]
            ensemble_prob = prediction_1
            """locals()['res' + str(i)] = dict([[x,  "{:4.4f}".format(y)] for x, y in zip(labels, ensemble_prob)])
            posted['res' + str(i)] = locals()['res' + str(i)]"""
        pos = ensemble_prob.index(max(ensemble_prob))
        major_value = labels[pos] +":  " +str(max(ensemble_prob))
        posted['major_value'] = major_value
        return render(request,'atma/results_overlay.html',{'posted': posted})
    except:
        return render(request,'atma/fail2.html')

@csrf_exempt
def videolimit(request):
    if not VideoUser.objects.filter(User=user).exists():
        vid_user = VideoUser(User=user,LastDateUsed=datetime.date.today(),TimesUsedToday=0)
        vid_user.save()
    vid_user = VideoUser.objects.get(User=user)
    subs = 0
    if vid_user.LastDateUsed == datetime.date.today():
        subs = vid_user.TimesUsedToday
    vid_user.LastDateUsed = datetime.date.today()
    vid_user.TimesUsedToday +=1

    if subs > 2 and not request.user.is_superuser:
        return HttpResponse('true')
    return HttpResponse('false')

@csrf_exempt
@login_required
def forum(request):
    if request.method == 'POST':
        threadForm = ThreadForm(request.POST)
        commentForm = CommentForm(request.POST)
        if threadForm.is_valid():
            submitted_thread = Thread(Title=threadForm.cleaned_data['Title'],
                                  Description=threadForm.cleaned_data['Description'],
                                  User=get_user(request),
                                  Topic=threadForm.cleaned_data['Topic'])
            submitted_thread.save()
        elif commentForm.is_valid():
            submitted_comment = Comment(Description=commentForm.cleaned_data['Description'],
                                        User=get_user(request),
                                        Thread=Thread.objects.get(pk = commentForm.cleaned_data['Thread']))
            submitted_comment.save()
        else:
            print('neither form is valid')

    threadForm = ThreadForm()
    commentForm = CommentForm()

    threads = Thread.objects.all()
    data = serialize('json', threads)
    threads = json.loads(data)

    comms = Comment.objects.all()
    data2 = serialize('json', comms)
    comms = json.loads(data2)

    return render(request, 'atma/forum.html', {'threads': threads, 'threadForm':threadForm, 'commentForm': commentForm, 'comments':comms})

@login_required
def delete_thread(request, pk):
    print('we are now in delete_thread')
    Thread.objects.filter(pk=pk).delete()
    return forum(request)

@csrf_exempt
def comments(request,thread_id):
    assigned_thread = Thread.objects.get(id=thread_id)
    title = assigned_thread.Title
    desc = assigned_thread.Description
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            submitted_comment = Comment(Description=form.cleaned_data['Description'],User=get_user(request),Thread=assigned_thread)
            submitted_comment.save()

    threadForm = ThreadForm()
    commentForm = CommentForm()
    threads = Thread.objects.all()
    data = serialize('json', threads)
    threads = json.loads(data)
    comms = Comment.objects.all()
    comms = serialize('json', comms)
    return render(request, 'atma/forum.html', {'threads': threads, 'threadForm':threadForm, 'commentForm': commentForm, 'comments':comms})


@csrf_exempt
def userVideo(request):
    data = {}
    if request.method == "POST":
        form = UserVideoForm(request.POST,request.FILES)
        print(form.is_valid())
        print(form.errors.as_data())
        if form.is_valid():
            video = form.cleaned_data['video']
            blob = bucket.blob(str(1)+".mp4")
            blob.upload_from_file(video)
            gcs_url = blob.public_url
            tracked_video = videoProcessing(video.temporary_file_path())
            data["video_src"] = tracked_video
    form = UserVideoForm()
    data["form"] = form
    return render(request,'atma/userVideo.html',data)

def forgot(request):
    #Must CHANGE THIS
    context = {}
    return render(request, 'atma/forgot_password_01.html', context)