from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import QuizSchedule
import pandas as pd
from datetime import timedelta

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            process_files(request.FILES['class_timetable'], request.FILES['faculty_file'])
            return redirect('download_schedule')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def process_files(class_timetable, faculty_file):
    # Read the uploaded Excel files
    class_df = pd.read_excel(class_timetable, header=None)  # Assuming no header in class timetable
    faculty_df = pd.read_excel(faculty_file)
    
    # Check required columns in faculty file
    required_faculty_columns = ['Subject Code', 'Faculty 1', 'Faculty 2']
    if not all(col in faculty_df.columns for col in required_faculty_columns):
        raise ValueError("Faculty file is missing required columns.")
    
    # Generate quiz slots
    quiz_slots = generate_quiz_slots()

    # Process the class timetable
    for index, row in class_df.iterrows():
        for subject_code in row:  # Iterate over each subject code in the row
            # Ensure we can find the subject code in the faculty file
            faculty_info = faculty_df[faculty_df['Subject Code'] == subject_code]
            if not faculty_info.empty:
                faculties = faculty_info[['Faculty 1', 'Faculty 2']].values[0]
                # Schedule quiz
                schedule_quiz(subject_code, faculties, quiz_slots)
            else:
                print(f"Subject Code {subject_code} not found in Faculty File.")  # Debugging line


def generate_quiz_slots():
    # Generate 15-minute intervals between 10 AM and 6 PM, excluding 1 PM to 2 PM
    start_time = pd.to_datetime("10:00:00")
    end_time = pd.to_datetime("18:00:00")
    break_start = pd.to_datetime("13:00:00")
    break_end = pd.to_datetime("14:00:00")

    slots = []
    while start_time < end_time:
        if not (break_start <= start_time < break_end):
            slots.append(start_time.time())
        start_time += timedelta(minutes=15)
    
    return slots

def schedule_quiz(subject_code, faculties, quiz_slots):
    for slot in quiz_slots:
        # Check if faculties are available for this slot and schedule the quiz
        QuizSchedule.objects.create(
            subject_name=subject_code,
            quiz_date='2024-10-04',  # This could be dynamic, based on user input
            quiz_time=slot,
            faculty_1=faculties[0],
            faculty_2=faculties[1]
        )
        # Remove the slot to avoid double-booking
        quiz_slots.remove(slot)
        return True  # Return True when quiz is scheduled
    return False  # Return False if no slot was available

def download_schedule(request):
    # Export the quiz schedule to Excel
    quizzes = QuizSchedule.objects.all()
    df = pd.DataFrame(list(quizzes.values('subject_name', 'quiz_date', 'quiz_time', 'faculty_1', 'faculty_2')))
    
    # Filter out duplicate subject codes (each subject appears only once)
    df = df.drop_duplicates(subset=['subject_name'])

    # Create the Excel file response
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="quiz_schedule.xlsx"'
    df.to_excel(response, index=False)
    return response
