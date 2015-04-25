from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from anon.models import AnonPost, AnonCommit
from anon.forms import AnonPostForm, AnonCommitForm

