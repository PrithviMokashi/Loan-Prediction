from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import LoanData
import pandas as pd
from xgboost import XGBClassifier

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
        user_id = int(request.POST['id'])

        loan_limit_get = request.POST.get('loanlimit')
        loan_limit = 1 if loan_limit_get == 'ncf' else 0

        gender=request.POST.get('gender')
        gender_dict = {'male':0,'female':0,'other':0,'prefernottosay':0}
        if gender in gender_dict:
            gender_dict[gender] += 1

        approve_get=request.POST.get('approved')
        approve = 1 if approve_get == 'yes' else 0

        loan_type=request.POST.get('loantype')
        loan_type_dict = {'type1':0, 'type2':0, 'type3':0}
        if loan_type in loan_type_dict:
            loan_type_dict[loan_type] += 1

        neg_ammor_get = request.POST.get('negammor')
        neg_ammor = 1 if neg_ammor_get == 'no' else 0

        int_only_get = request.POST.get('intonly')
        int_only = 1 if int_only_get == 'notint' else 0

        lump_sum_get = request.POST.get('lumpsum')
        lump_sum = 1 if lump_sum_get == 'notlump' else 0

        property_value = int(request.POST['propval'])

        const_type_get = request.POST.get('consttype')
        const_type = 1 if const_type_get == 'sb' else 0

        occupancy_type = request.POST.get('occtype')
        occupancy_type_dict = {'pr':0, 'sr':0, 'ir':0}
        if occupancy_type in occupancy_type_dict:
            occupancy_type_dict[occupancy_type] += 1

        secured_by_get = request.POST.get('secby')
        secured_by = 0 if secured_by_get == 'home' else 1

        total_units = request.POST.get('totunit')
        total_units_dict = {'1u':0, '2u':0, '3u':0, '4u':0}
        if total_units in total_units_dict:
            total_units_dict[total_units] += 1

        income = int(request.POST['income'])

        credit_type = request.POST.get('credtype')
        credit_type_dict = {'exp':0, 'equi':0, 'crif':0, 'cib':0}
        if credit_type in credit_type_dict:
            credit_type_dict[credit_type] += 1

        credit_score = int(request.POST['credscore'])

        security_type_get = request.POST.get('sectype')
        security_type = 1 if security_type_get == 'direct' else 0

        loan_purpose = request.POST.get('loanpur')
        loan_purpose_dict = {'p1':0, 'p2':0, 'p3':0, 'p4':0}
        if loan_purpose in loan_purpose_dict:
            loan_purpose_dict[loan_purpose] += 1

        cred_worthiness_get = request.POST.get('credworth')
        cred_worthiness = 1 if cred_worthiness_get == 'l2' else 0

        open_credit_get = request.POST.get('opencred')
        open_credit = 1 if open_credit_get == 'open' else 0

        business_get = request.POST.get('business')
        business = 1 if business_get == 'no' else 0

        loan_amount = int(request.POST['loanamt'])

        rate_interest = float(request.POST['rateint'])

        int_ratespread = float(request.POST['ratespread'])

        upfront_charges = float(request.POST['upfront'])

        term = int(request.POST['term'])

        cocred_type_get = request.POST.get('cocredtype')
        cocred_type = 1 if cocred_type_get == 'exp' else 0

        age = request.POST.get('age')
        age_dict = {'25':0, '34':0, '44':0, '54':0, '64':0, '74':0, '80':0}
        if age in age_dict:
            age_dict[age] += 1

        appsub_get = request.POST.get('subapp')
        appsub = 1 if appsub_get == 'inst' else 0

        loan_toval = float(request.POST['ltv'])

        region = request.POST.get('region')
        region_dict = {'south':0, 'north':0, 'central':0, 'northeast':0}
        if region in region_dict:
            region_dict[region] += 1

        deptinc_ratio = int(request.POST['dtir'])

        dataset = pd.read_csv(r"static/datasets/cleaned_dataset.csv")
        # dataset = dataset.drop(['Male', 'Female', 'Joint', 'Sex Not Available'], axis=1)
        
        X_train = dataset[["id","loan_amount","rate_of_interest","interest_rate_spread","upfront_charges","term",
                            "property_value","income","credit_score","ltv","dtir1","loan_limit","approv_in_adv",
                            "credit_worthiness","open_credit","business_or_commercial","neg_ammortization","interest_only",
                            "lump_sum_payment","construction_type","secured_by","co-applicant_credit_type",
                            "submission_of_application","security_type","type1","type2","type3","p1","p2","p3","p4","ir","pr",
                            "sr","U1","U2","U3","U4","CIB","CRIF","EQUI","EXP","age_25-34","age_35-44","age_45-54","age_55-64",
                            "age_65-74","under_25","over_74","North","North-East","central","south"]]
        Y_train = dataset[["status"]]

        xgbc = XGBClassifier()
        xgbc.fit(X_train, Y_train)

        data_to_predict = [[user_id, loan_amount, rate_interest, int_ratespread, upfront_charges, term, property_value,
                                income, credit_score, loan_toval, deptinc_ratio, loan_limit, approve,
                                cred_worthiness, open_credit, business, neg_ammor, int_only, lump_sum, const_type,
                                secured_by, cocred_type, appsub, security_type, loan_type_dict['type1'], loan_type_dict['type2'],
                                loan_type_dict['type3'], loan_purpose_dict['p1'], loan_purpose_dict['p2'], loan_purpose_dict['p3'],
                                loan_purpose_dict['p4'], occupancy_type_dict['ir'], occupancy_type_dict['pr'], occupancy_type_dict['sr'],
                                total_units_dict['1u'], total_units_dict['2u'], total_units_dict['3u'], total_units_dict['4u'],
                                credit_type_dict['cib'], credit_type_dict['crif'], credit_type_dict['equi'], credit_type_dict['exp'],
                                age_dict['34'], age_dict['44'], age_dict['54'], age_dict['64'], age_dict['74'], age_dict['25'],
                                age_dict['80'], region_dict['north'], region_dict['northeast'], region_dict['central'], region_dict['south']
                            ]]
        
        xgb_column_features = ["id","loan_amount","rate_of_interest","interest_rate_spread","upfront_charges","term",
                            "property_value","income","credit_score","ltv","dtir1","loan_limit","approv_in_adv",
                            "credit_worthiness","open_credit","business_or_commercial","neg_ammortization","interest_only",
                            "lump_sum_payment","construction_type","secured_by","co-applicant_credit_type",
                            "submission_of_application","security_type","type1","type2","type3","p1","p2","p3","p4","ir","pr",
                            "sr","U1","U2","U3","U4","CIB","CRIF","EQUI","EXP","age_25-34","age_35-44","age_45-54","age_55-64",
                            "age_65-74","under_25","over_74","North","North-East","central","south"]

        df = pd.DataFrame(data_to_predict , columns = xgbc.feature_names_in_)

        prediction_result = xgbc.predict(df)

        predict = LoanData.objects.create(
            user_id = user_id,
            loan_amount = loan_amount,
            rate_of_interest = rate_interest,
            upfront_charges = upfront_charges,
            term = term,
            property_value = property_value,
            income = income,
            credit_score = credit_score,
            ltv = loan_toval,
            status = prediction_result,
            dtir1 = deptinc_ratio,
            loan_limit = loan_limit,
            approv_in_adv = approve,
            credit_worthiness = cred_worthiness,
            open_credit = open_credit,
            business_or_comm = business,
            neg_ammor = neg_ammor,
            interest_rate_spread = int_ratespread,
            interest_only= int_only,
            lump_sum = lump_sum,
            construction_type = const_type,
            secured_by = secured_by,
            coapp_credit_type = cocred_type,
            submission_of_app = appsub,
            security_type = security_type,
            type1 = loan_type_dict['type1'],
            type2 = loan_type_dict['type2'],
            type3 = loan_type_dict['type3'],
            p1 = loan_purpose_dict['p1'],
            p2 = loan_purpose_dict['p2'],
            p3 = loan_purpose_dict['p3'],
            p4 = loan_purpose_dict['p4'],
            ir = occupancy_type_dict['ir'],
            pr = occupancy_type_dict['pr'],
            sr = occupancy_type_dict['sr'],
            u1 = total_units_dict['1u'],
            u2 = total_units_dict['2u'],
            u3 = total_units_dict['3u'],
            u4 = total_units_dict['4u'],
            cib = credit_type_dict['cib'],
            crif = credit_type_dict['crif'],
            equi = credit_type_dict['equi'],
            exp = credit_type_dict['exp'],
            age_25 = age_dict['34'],
            age_35 = age_dict['44'],
            age_45 = age_dict['54'],
            age_55 = age_dict['64'],
            age_65 = age_dict['74'],
            age_under_25 = age_dict['25'],
            age_over_74 = age_dict['80'],
            north = region_dict['north'],
            north_east = region_dict['northeast'],
            central = region_dict['central'],
            south = region_dict['south']
        )
        predict.save()
        passed = "User will not default on Loan"
        failed = "User will default"
        result = ""
        if prediction_result[0] == 1:
            result = passed
        else:
            result = failed
        
        return render(request, "inputform.html", {
            "status":result
        })
        