from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .migrations import *
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from utils.helpers import *
from project_app.models import *
from datetime import datetime,timedelta
from django.conf import settings

@csrf_exempt
@api_view(['POST'])
def user_register(request):
    mobile_number = request.data.get('mobile_number')

    if mobile_number == '' or mobile_number is None:
        return Response({"message":'Please Provide Mobile'},status=status.HTTP_400_BAD_REQUEST)
    
    if len(mobile_number) != 10:
        return Response({"message":"Please provide valid mobile number Your mobile number is too sort"},status=status.HTTP_400_BAD_REQUEST)
    
    if UserProfile.objects.filter(mobile_number = mobile_number).exists():
        return Response({'message':'This Mobile Number is Already Registerd in Our Portal'},status=status.HTTP_400_BAD_REQUEST)
    user_name = generate_random_number()
    user = User.objects.create_user(username=user_name)
    user_profile = UserProfile.objects.create(user = user,mobile_number = mobile_number)
    otp = generate_otp()
    account_otp = Account_Otp()
    account_otp.user = user_profile.user
    account_otp.otp = otp
    account_otp.save()
    return Response({'message':"We are sending an otp,please varify for further process",'otp':otp},status=status.HTTP_200_OK)



@csrf_exempt
@api_view(['POST'])
def account_otp_varify(request):
    otp = request.data.get('otp')
    
    mobile_number =request.data.get('mobile_number')
    user_profile = UserProfile.objects.filter(mobile_number = mobile_number).first()


    account_otp = Account_Otp.objects.filter(user = user_profile.user,otp = otp).first()
   
    if account_otp.otp == int(otp):
        Account_Otp.objects.filter(user = user_profile.user,otp = otp).delete()
        return Response({"message":'Otp varification Done '},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message":'Invalid Otp'},status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def add_username_profile(request):
    mobile_number = request.data.get('mobile_number')
    first_name = request.data.get('first_name')
    last_name = request.data.get("last_name")

    if first_name == '' or first_name is None:
        return Response({"messgae":'Please provide first name'},status=status.HTTP_400_BAD_REQUEST)
    
    if last_name == '' or last_name is None:
        return Response({"messgae":'Please provide last_name'},status=status.HTTP_400_BAD_REQUEST)
    
    user_profile = UserProfile.objects.filter(mobile_number = mobile_number).first()
    user = User.objects.get(id = user_profile.user.id) 
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return Response({"message":'Registration comlete,Please Login for use App'},status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
def user_login(request):
    mobile_number = request.data.get('mobile_number')
    if not UserProfile.objects.filter(mobile_number = mobile_number).exists():
        return Response({"messge":'Please registerd mobile number'},status=status.HTTP_400_BAD_REQUEST)
    otp = generate_otp()

    user_profile = UserProfile.objects.filter(mobile_number = mobile_number).first()
    account_otp = Lgin_otp()
    account_otp.otp = otp
    account_otp.user = user_profile.user
    account_otp.save()
    return Response({'message':"We are sending an otp,please varify for complete login",'otp':otp},status=status.HTTP_200_OK)



@csrf_exempt
@api_view(['POST'])
def login_otp_varify(request):
    otp = request.data.get('otp')
    mobile_number =request.data.get('mobile_number')
    user_profile = UserProfile.objects.filter(mobile_number = mobile_number).first()

    account_otp = Lgin_otp.objects.filter(user = user_profile.user,otp = otp).first()
    user_name = account_otp.user.first_name+' '+account_otp.user.last_name
    if account_otp.otp == int(otp):
        Lgin_otp.objects.filter(user = user_profile.user,otp = otp).delete()
        return Response({"message":F'Welcome {user_name} '},status=status.HTTP_200_OK)
    else:
        return Response({"message":'Invalid Otp'},status=status.HTTP_400_BAD_REQUEST)
    

@csrf_exempt
@api_view(['GET'])
def show_all_images(request):
    all_images_data = All_Images.objects.filter().values()
    return Response({"data":all_images_data},status=status.HTTP_200_OK)



def hello(request):
    return Response("hi")


@csrf_exempt
@api_view(['POST'])
def user_image_recongnization(request):
    current_date = datetime.now()
   
    user_actoin = request.data.get('user_action')  # 0- left swipe ,1- right swipe
    user_id = request.data.get('user_id')
    image_id = request.data.get('image_id')
    imags_id_list = UserHistory.objects.filter(user__id = user_id,click_time__icontains= current_date.date())
   
    blank_list = []
    for i in imags_id_list:
        blank_list.append((i.all_images.id))
    all_images_id = All_Images.objects.values_list('id').distinct()
    user_data = User.objects.get(id = user_id)
    
    user_name = user_data.first_name+''+user_data.last_name
    if  len(all_images_id) == len(list(set(blank_list))):
        return Response({'message':F'{user_name} You have rated all the images'},status=status.HTTP_200_OK)
        
    else:
        # for rejected images
        if int(user_actoin) == 0 :
            user = user_id
            image_data = All_Images.objects.get(id = image_id)
            user_data = User.objects.get(id = user_id)
            RejectedImages.objects.create(user = user_data,images_id = image_id)
            user_name = user_data.first_name+''+user_data.last_name
            UserHistory.objects.create(user = user_data,all_images = image_data,is_reject = True)
            return Response({'message':F'{user_name} You have rejected {image_data.image_name}'},status=status.HTTP_200_OK)
        elif int(user_actoin) == 1 :
            user = user_id
            image_data = All_Images.objects.get(id = image_id)
            user_data = User.objects.get(id = user_id)
            InterstedImages.objects.create(user = user_data,images_id = image_id)
            user_name = user_data.first_name+''+user_data.last_name
            UserHistory.objects.create(user = user_data,all_images = image_data,is_selected = True)
            return Response({'message':F'{user_name} You have selected {image_data.image_name}'},status=status.HTTP_200_OK)
        return Response({"message":'You Choose Wrong swipe'},status=status.HTTP_400_BAD_REQUEST)
    
    


@csrf_exempt
@api_view(['GET'])
def get_user_history(request):
    user_id = request.query_params['user_id']
    try:
        history_data = UserHistory.objects.filter(user__id = user_id)
        data_list = []
        for i in history_data:
            dict1 = {}
            dict1['user_id'] = i.user.id
            image = settings.BASE_URL+"media/"+str(i.all_images.image)
            dict1['image'] = image
            dict1['image_name'] = i.all_images.image_name
            if i.is_reject == True:
                dict1['image_status'] = "rejected"
            else:
                dict1['image_status'] = "selected"
            dict1['activity_date'] = i.click_time.date()
            dict1['activity_time'] = i.click_time.time()
            data_list.append(dict1)

        return Response({"message":data_list},status=status.HTTP_200_OK)
    except UserHistory.DoesNotExist:
        return Response({"data does Not exist"},status=status.HTTP_204_NO_CONTENT)
    




@csrf_exempt
@api_view(['GET'])
def get_user_profile(request):
    user_id = request.query_params['user_id']

    try:
        user_profile = UserProfile.objects.filter(user__id = user_id).first()

        data = {}

        data['username'] = user_profile.user.first_name+user_profile.user.last_name
        data['mobile_number'] = user_profile.mobile_number
        data['profile_image'] =  str(user_profile.profile_image.url)

        return Response({'data':data},status=status.HTTP_200_OK)

    except UserProfile.DoesNotExist:
        return Response({"message":'Please provide valid user id'},status=status.HTTP_400_BAD_REQUEST)
    
    

    # uri = "s3://singh1234buck/media/profile_images/"