from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from anon.models import AnonPost, AnonCommit
from anon.forms import AnonPostForm, AnonCommitForm


class AnonFrontView(ListView):
	template_name = 'anon/front.html'
	queryset = AnonPost.objects.published()
	paginate_by = 5


class AnonPostCommitView(CreateView):
	template_name = 'anon/post_detail.html'
	form_class = AnonCommitForm

	def get_context_data(self, **kwargs):
		context = super(AnonPostCommitView, self).get_context_data(**kwargs)
		pk, slug = self.kwargs['pk'], self.kwargs['slug']
		context['object'] = AnonPost.objects.by_post(pk, slug)
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.post = AnonPost.objects.get(postid=self.kwargs['pk'])
		obj.save()
		obj.post.last_commited = obj.created
		obj.post.commit_number += 1
		obj.post.save()
		return HttpResponseRedirect(obj.get_absolute_url())


class AnonCreatePostView(CreateView):
	template_name = 'anon/post_create.html'
	form_class = AnonPostForm