from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django import forms
from elearn.models import Lesson

from elearn.models import (Answer, Question, Learner, LearnerAnswer,
                              Course, User, Announcement)
from .models import Timetable, Course, Instructor




class PostForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('content', )

class ProfileForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput())
    confirm_email=forms.EmailField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',

        ]

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if email != confirm_email:
            raise forms.ValidationError(
                "Emails must match!"
            )



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email') 


class InstructorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
            super(InstructorSignUpForm, self).__init__(*args, **kwargs)

            for fieldname in ['username', 'password1', 'password2']:
                self.fields[fieldname].help_text = None
                    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_instructor = True
        if commit:
            user.save()
        return user



class LearnerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='First name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last name')
    email = forms.EmailField(required=True, help_text='Email address')
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True, help_text='Select a course')
    interests = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_learner = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        learner = Learner.objects.create(user=user, course=self.cleaned_data.get('course'))
        learner.interests.add(*self.cleaned_data.get('interests'))
        return user



class LearnerInterestsForm(forms.ModelForm):
    class Meta:
        model = Learner
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = LearnerAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')


class LearnerCourse(forms.ModelForm):
    class Meta:
        model = Learner
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }

    @transaction.atomic
    def save(self):
        learner = Learner()
        learner.interests.add(*self.cleaned_data.get('interests'))
        return learner_id

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'day_of_week', 'start_time', 'end_time', 'google_meet_link', 'instructor']

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['day_of_week', 'start_time', 'end_time', 'subject', 'instructor', 'location', 'google_meet_link']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'instructor': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'google_meet_link': forms.URLInput(attrs={'class': 'form-control'}),
        }