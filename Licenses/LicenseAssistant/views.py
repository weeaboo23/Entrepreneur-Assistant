from django.shortcuts import render 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect 
from django.urls import reverse 
from django.shortcuts import redirect
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import re
import json
from . models import User ,ApprovalInfo, Approval ,AILearningExample , ApprovalMapping , ContactMessage ,Application
from openai import OpenAI
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")

)
client2 = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY2"),
    base_url=os.getenv("OPENAI_BASE_URL")

)


    
def get_license_suggestions(structure, activity, location):
    prompt = f"Given the following business structure: {structure}, activity: {activity}, and location: {location}, list the licenses or approvals required for starting the business in India. Please return them in a simple list, separated by commas."

    try:
        response = client.chat.completions.create(model="gryphe/mythomax-l2-13b", 
        messages=[{"role": "system", "content": "You are an expert in Indian business regulations."},
                  {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000)

        suggestions = response.choices[0].message.content.strip()
        
        # Ensuring the response is returned as a clean list of license names
        suggestions_list = [name.strip() for name in suggestions.split(",")]

        # Further cleaning by removing unwanted characters or text
        cleaned_suggestions = []
        for name in suggestions_list:
            name = name.strip()
            if name:
                cleaned_suggestions.append(name)
        
        return cleaned_suggestions

    except Exception as e:
        return f"Error: {str(e)}"
    
def get_license_info_(Approval_name , location):


    prompt = f"""Give me the following information about the license named '{Approval_name} applicable in state '{location} :
    1. A short description of what this license is.
    2. List of documents required to apply for this license.
    3. Official link (working and direct, not just homepage) where a user can apply for it.
    4. The Department which Issues the License

    Format the response in JSON like:
    {{
        "description": "...",
        "documents_required": ["doc1", "doc2", "doc3"],
        "application_link": "https://...",
        "Department" : "..."
    }}
    """
    try:
        response = client2.chat.completions.create(model="gryphe/mythomax-l2-13b", 
        messages=[{"role": "system", "content": "You are an expert in Indian business regulations."},
                  {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=10000)

        ai_info = response.choices[0].message.content.strip()
        approval, created = Approval.objects.get_or_create(name=Approval_name)
    
        approval_info = json.loads(ai_info)
        information , created = ApprovalInfo.objects.get_or_create(
            approval=approval,
            description=approval_info.get("description", ""),
            documents_required=approval_info.get("documents_required", []),
            application_link=approval_info.get("application_link", ""),
            department=approval_info.get("Department", "")
        )
        information.save()

        return information 
    except json.JSONDecodeError:
        return f"Error: Failed to parse response into JSON. Response: {ai_info}"

    except Exception as e:
        return f"Error: {str(e)}"
    

        
        






    
def extract_licenses_from_ai_response(ai_response):
    cleaned_response = re.sub(r"^.*?the following licenses or approvals are required:", "", ai_response, flags=re.DOTALL)
    license_pattern = re.compile(r"\d+\.\s*(.*?)\n")
    licenses = license_pattern.findall(cleaned_response)
    cleaned_licenses = [license.strip() for license in licenses]
    
    return cleaned_licenses



def clean_input(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text



def fuzzy_lookup_mapping(structure, activity, location, threshold=85):
    """
    Returns an existing mapping that closely matches the input data.
    """
    all_mappings = ApprovalMapping.objects.all()

    structure_input = clean_input(structure)
    activity_input = clean_input(activity)
    location_input = clean_input(location)

    for mapping in all_mappings:
        s_score = fuzz.token_sort_ratio(clean_input(mapping.structure), structure_input)
        a_score = fuzz.token_sort_ratio(clean_input(mapping.activity), activity_input)
        l_score = fuzz.token_sort_ratio(clean_input(mapping.location), location_input)

        if s_score >= threshold and a_score >= threshold and l_score >= threshold:
            return mapping
    return None

def get_fuzzy_matched_approval(name, threshold=85):
    """
    Returns an existing approval if one is found with a sufficient fuzzy match.
    """
    approvals = Approval.objects.all()
    for approval in approvals:
        score = fuzz.token_sort_ratio(name.lower(), approval.name.lower())
        if score >= threshold:
            return approval
    return None





# Create your views here.
def index(request):
    return render(request , "LicenseAssistant/index.html")




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "LicenseAssistant/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "LicenseAssistant/login.html")


def createAccount(request):
     if request.method == "POST":
        username = request.POST["Username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm_password"]
        if password != confirmation:
            return render(request, "LicenseAssistant/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "LicenseAssistant/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
     else:
        return render(request, "LicenseAssistant/register.html")

def logout_view(request):
    request.session.pop('licenses', None)
    request.session.pop('structure', None)
    request.session.pop('activity', None)
    request.session.pop('ai_suggestions', None)
    request.session.pop('location', None)
    logout(request)
    return HttpResponseRedirect(reverse("login"))





def licenseSearch(request):
    if request.method == "POST":
        structure = request.POST.get("structure")
        activity = request.POST.get("activity")
        location = request.POST.get("location")

        ai_suggestions = get_license_suggestions(structure, activity, location)
        license_list = extract_licenses_from_ai_response(' '.join(ai_suggestions))

        AILearningExample.objects.create(
            structure=structure,
            activity=activity,
            location=location,
            suggested_licenses=json.dumps(license_list)
            )


        approval_object = []
        for name in license_list:
            existing_approval = get_fuzzy_matched_approval(name)
            if existing_approval:
                approval_object.append(existing_approval)
            else:
                approval, created = Approval.objects.get_or_create(name__iexact=name,defaults={'name': name})
                approval_object.append(approval)
        
        mapping, created = ApprovalMapping.objects.get_or_create(
            structure=structure,
            activity=activity,
            location=location
            )
        for approval in approval_object:
            if approval not in mapping.licenses.all():
                mapping.licenses.add(approval)

        mapping.save()

        request.session['licenses'] = [lic.id for lic in mapping.licenses.all()]
        request.session['structure'] = structure
        request.session['activity'] = activity
        request.session['location'] = location
        request.session['ai_suggestions'] = ai_suggestions
        return redirect('license_results')
    
    return render(request, "LicenseAssistant/license.html")


def licenseSearchResults(request):
    license_ids = request.session.get('licenses', [])
    licenses = Approval.objects.filter(id__in=license_ids)
    # Retrieve the search results and input data from the session
    structure = request.session.get('structure', '')
    activity = request.session.get('activity', '')
    location = request.session.get('location', '')
    ai_suggestion = request.session.get('ai_suggestions','')

    # Render the result page with the session data
    return render(request, "LicenseAssistant/license_results.html", {
        "licenses": licenses,
        "structure": structure,
        "activity": activity,
        "location": location,
        "ai_suggestions": ai_suggestion
    })

def license_details(request , slug):
    license = Approval.objects.get(slug=slug)
    location = request.session.get('location', '')
    get_license_info_(license.name , location)
    license_info = ApprovalInfo.objects.get(approval=license)
    return render(request , "LicenseAssistant/License_details.html",{
        "info": license_info,
        "location": location

    })
     

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your message'}))
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your email'}))


def contact_me(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Store the contact message
            ContactMessage.objects.create(
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                user_email=form.cleaned_data['user_email'],
                user=request.user if request.user.is_authenticated else None
            )
            return redirect('thank_you')  # Redirect to a thank you page after submission

    else:
        form = ContactForm()

    return render(request, 'LicenseAssistant/contact_me.html', {'form': form})




def track_applications(request):
    if request.user.is_authenticated:
        applications = Application.objects.filter(user=request.user)
        return render(request, 'LicenseAssistant/track_applications.html', {'applications': applications})
    else:
        return redirect('login')
    




class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Current password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}))

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps the user logged in after password change
            return redirect('password_change_done')  # Redirect to a success page
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'LicenseAssistant/change_password.html', {'form': form})