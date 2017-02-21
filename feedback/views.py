from django.shortcuts import render
from django.template import RequestContext
from feedback.forms import FeedbackForm
import datetime


def feedback(request):
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST, label_suffix='')
        if feedback_form.is_bound and feedback_form.is_valid():
            feedback_form.save(commit=False)
            feedback_form.datetime = datetime.now()
            feedback_form.user = request.user
    else:
        feedback_form = FeedbackForm(label_suffix='')

    return render(request, 'feedback.html', context={'form': feedback_form})
