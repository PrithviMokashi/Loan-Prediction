from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import LoanData

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def inputform(request):
    return render(request,'inputform.html')

def login(request):
    if request.method == "POST":
        uname=request.POST['luser'].lower()
        pass1=request.POST['lpass'].lower()
        user = authenticate(username=uname, password=pass1)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid Credentials")
            return render(request, "login.html")
    return render(request,'login.html')

def register(request):
    if request.method=="POST":
        username = (request.POST['user']).lower()
        fname = request.POST['fname'].lower()
        lname = request.POST['lname'].lower()
        email = request.POST['email']
        passwd = request.POST['pass']
        con_passwd = request.POST['confirm_pass']
            
        if passwd==con_passwd:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists!")
                return render(request, "register.html")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists!")
                return render(request, "register.html")
            else:
                user = User.objects.create_user(username=username, first_name=fname,
                last_name=lname, email=email, password=passwd)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"Password's do not match!")
            return render(request,"register.html")
    else:
        return render(request, "register.html")
    return render(request,'register.html')

def predictLoan(request):
    if request.method == 'POST':
        userid=request.POST['id']
        loanlimit=request.POST.get('loanlimit')
        gender=request.POST.get('gender')
        approve=request.POST.get('approved')
        loantype=request.POST.get('loantype')
        negammor=request.POST.get('negammor')
        intonly=request.POST.get('intonly')
        lumpsum=request.POST.get('lumpsum')
        propertyvalue=request.POST['propval']
        consttype=request.POST.get('consttype')
        occupancytype=request.POST.get('occtype')
        securedby=request.POST.get('secby')
        totalunits=request.POST.get('totunit')
        income=request.POST['income']
        credittype=request.POST.get('credtype')
        creditscore=request.POST['credscore']
        securitytype=request.POST.get('sectype')
        loanpurpose=request.POST.get('loanpur')
        credworthiness=request.POST.get('credworth')
        opencredit=request.POST.get('opencred')
        business=request.POST.get('business')
        loanamount=request.POST.get('loanamt')
        rateinterest=request.POST['rateint']
        intratespread=request.POST['ratespread']
        upfrontcharges=request.POST['upfront']
        term=request.POST['term']
        cocredtype=request.POST.get('cocredtype')
        age=request.POST.get('age')
        appsub=request.POST.get('subapp')
        loantoval=request.POST['ltv']
        region=request.POST.get('region')
        deptincratio=request.POST['dtir']


        predict = LoanData.objects.create(userid=userid, loanlimit=loanlimit, gender=gender, approve=approve, loantype=loantype, negammor=negammor, intonly=intonly, lumpsum=lumpsum, propertyvalue=propertyvalue, consttype=consttype, occupancytype=occupancytype, securedby=securedby, totalunits=totalunits, income=income, credittype=credittype, creditscore=creditscore, securitytype=securitytype, loanpurpose=loanpurpose, credworthiness=credworthiness, opencredit=opencredit, business=business, loanamount=loanamount, rateinterest=rateinterest, intratespread=intratespread, upfrontcharges=upfrontcharges, term=term, cocredtype=cocredtype, age=age, appsub=appsub, loantoval=loantoval, region=region, deptincratio=deptincratio)
        predict.save()
        return render(request, "predictloan.html", {"userid":userid, "loanlimit":loanlimit, "gender":gender, "approve":approve, "loantype":loantype, "negammor":negammor, "intonly":intonly, "lumpsum":lumpsum, "propertyvalue":propertyvalue, "consttype":consttype, "occupancytype":occupancytype, "securedby":securedby, "totalunits":totalunits, "income":income, "credittype":credittype, "creditscore":creditscore, "securitytype":securitytype, "loanpurpose":loanpurpose, "credworthiness":credworthiness, "opencredit":opencredit, "business":business, "loanamount":loanamount, "rateinterest":rateinterest, "intratespread":intratespread, "upfrontcharges":upfrontcharges, "term":term, "cocredtype":cocredtype, "age":age, "appsub":appsub, "loantoval":loantoval, "region":region, "deptincratio":deptincratio})
        