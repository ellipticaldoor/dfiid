from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from anon.models import AnonPost, AnonCommit
from anon.forms import AnonPostForm, AnonCommitForm


class AnonFrontView(ListView):
	template_name = 'anon/front.html'
	# REVISAR!!!!
	# queryset = AnonPost.objects.last_commited()
	paginate_by = 5

	def get(self, request, *args, **kwargs):
		if request.is_ajax(): self.template_name = 'ajax/anon_post_list.html'
		return super(AnonFrontView, self).get(request, *args, **kwargs)

	def get_queryset(self):
		if self.kwargs['tab'] == 'top': return AnonPost.objects.last_commited()
		else: return AnonPost.objects.created()

	def get_context_data(self, **kwargs):
		context = super(AnonFrontView, self).get_context_data(**kwargs)
		context['list_url'] = '/anon'
		context['tab_show'] = self.kwargs['tab']
		if self.kwargs['tab'] == 'top': context['list_url'] = '/anon'
		else: context['list_url'] = '/anon/new'
		return context


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