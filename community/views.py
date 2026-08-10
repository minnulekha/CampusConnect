from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import FacultyProfile
from .models import LocationQuestion, LocationReply, Notification
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() # Load environment variables from .env file

@login_required
def ask_location(request, faculty_id):
    faculty = get_object_or_404(FacultyProfile, id=faculty_id)
    if request.method == "POST":
        text = request.POST.get('question_text', '').strip()
        if text:
            # Create the question instance
            LocationQuestion.objects.create(
                user=request.user,
                faculty=faculty,
                text=text
            )
    return redirect('faculty:profile', pk=faculty_id)

@login_required
def reply_location(request, question_id):
    question = get_object_or_404(LocationQuestion, id=question_id)
    if request.method == "POST":
        reply_text = request.POST.get('reply_text', '').strip()
        if reply_text:
            LocationReply.objects.create(
                question=question,
                user=request.user,
                info_source=reply_text
            )
            
            # Send notification alert to the question creator if someone else replies
            if question.user != request.user:
                Notification.objects.create(
                    user=question.user,
                    message=f"{request.user.username} replied to your location question regarding Dr. {question.faculty.user.last_name}!"
                )
                
            # Also safely flag the faculty member's source as a student report tracking update
            fac_prof = question.faculty
            fac_prof.current_location_string = f"Reported: {reply_text}"
            fac_prof.location_source = 'report'
            fac_prof.save()
            
    return redirect('faculty:profile', pk=question.faculty.id)

@login_required
def view_notifications(request):
    notes = request.user.notifications.all().order_by('-created_at')
    # Mark all as read upon opening this view page
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'community/notifications.html', {'notifications': notes})

def generate_faculty_summary(faculty_profile):
    """
    Gathers all community replies for a given faculty member and asks OpenAI
    to generate a scannable single-sentence location status summary.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_actual_openai_api_key_here":
        return "AI Summary unavailable: OpenAI API Key configuration missing."

    # Gather all replies linked to this faculty member's questions
    replies = LocationReply.objects.filter(question__faculty=faculty_profile).order_by('-created_at')[:5]
    
    if not replies.exists():
        return "No recent student reports available to summarize."

    # Build a text block of all recent crowd-sourced sightings
    reports_text = "\n".join([f"- User reported: {r.info_source} ({r.created_at.strftime('%H:%M')})" for r in replies])

    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using a highly cost-effective, blazing fast hackathon model
            messages=[
                {"role": "system", "content": "You are a helpful campus assistant. Summarize the provided crowd-sourced student location reports for a professor into a single, direct, action-oriented sentence. Clearly state where they were last seen and when. Do not invent details. If contradictory, state that it is unconfirmed."},
                {"role": "user", "content": f"Professor: Dr. {faculty_profile.user.last_name}\nRecent Sightings:\n{reports_text}"}
            ],
            max_tokens=100,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Could not generate summary details due to a connection timeout."