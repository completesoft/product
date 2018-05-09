from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Person, Residence_address, Experience, Education, MailToAddress, MailBackSettings, Location, CvState, CvStatusName
from django.core.mail import EmailMessage, get_connection
from .forms import PersonForm, ResidenceForm, EducationForm, ExpirienceForm
from django.forms import formset_factory, modelformset_factory
from .support_function import emailSenderTwo
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, BaseCreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.apps import apps
from .forms import FilterCvListForm, CvPersonForm, CvEducationForm, CvResidenceForm, CvExperienceForm, PersonForm, ResidenceForm, EducationForm, ExpirienceForm, CvStateForm
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404, HttpResponseNotFound
from django.core.exceptions import FieldError, ValidationError, ObjectDoesNotExist


def person(request, loc_id):
    try:
        location = Location.objects.get(loc_id=loc_id)
    except Location.DoesNotExist:
        raise Http404
    edu_prefix = 'education'
    exp_prefix = 'expirience'
    if request.method == 'POST':
        form = PersonForm(request.POST)
        formRes = ResidenceForm(request.POST)
        # formset
        EduFormSet = formset_factory(EducationForm, extra=0)
        edu_formset = EduFormSet(request.POST, prefix=edu_prefix)
        ExpFormSet = formset_factory(ExpirienceForm, extra=0)
        exp_formset = ExpFormSet(request.POST, prefix=exp_prefix)
        if form.is_valid() and formRes.is_valid() and exp_formset.is_valid() and edu_formset.is_valid():
            pers = form.save(location)
            CvState.objects.create(cv=pers, status=CvStatusName.objects.get(status=0))
            if formRes.has_changed():
                formRes.save(pers)
            for form in edu_formset:
                if form.has_changed():
                    form.save(pers)
            for form in exp_formset:
                if form.has_changed():
                    form.save(pers)
            mail_to = [email.email_address for email in location.mail_to.all()]
            if mail_to:
                mail = emailSenderTwo(mail_to, pers)
                pers.email_send = mail
                pers.save()
            return render(request, 'job/thanks.html', {'loc_id': loc_id})
    else:
        data_raw = {'{}-TOTAL_FORMS': '1', '{}-INITIAL_FORMS': '1', '{}-MAX_NUM_FORMS': ''}
        data_edu = {k.format(edu_prefix):v for k,v in data_raw.items()}
        data_exp = {k.format(exp_prefix):v for k,v in data_raw.items()}
        form = PersonForm()
        formRes = ResidenceForm()
        EduFormSet = formset_factory(EducationForm, extra=0)
        edu_formset = EduFormSet(data_edu, prefix=edu_prefix)
        ExpFormSet = formset_factory(ExpirienceForm, extra=0)
        exp_formset = ExpFormSet(data_exp, prefix='expirience')
    return render(request, 'job/index_set.html', {'form':form, 'formRes':formRes ,'edu_formset':edu_formset, 'exp_formset': exp_formset, 'loc_id': loc_id})


def server_response(request, mail_group=0):
    return HttpResponse("Online")


class CvList(ListView):
    model = Person
    context_object_name = 'persons'
    template_name = 'job/cv_list.html'
    allow_empty = True
    form = None

    def get(self, request, *args, **kwargs):
        filter_set = FilterCvListForm(request.GET)
        if filter_set.has_changed():
            self.form = filter_set
        return super(CvList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if self.form:
            self.form.is_valid()
            # фильруем все поля кроме статуса резюме
            query_set = self.model.objects.filter(**self.form.filter_set())
            # фильтруем по статусу
            if self.form.cleaned_data['cv_state']:
                int_set = list(map(int, self.form.cleaned_data['cv_state']))
                state_set = [pers.id for pers in query_set if pers.cv_state().status.status in int_set]
                query_set = query_set.filter(id__in=state_set)
        else:
            query_set = self.model.objects.all()
        return query_set

    def get_context_data(self, **kwargs):
        context = super(CvList, self).get_context_data(**kwargs)
        context['filter'] = self.form if self.form else FilterCvListForm()
        return context


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CvList, self).dispatch(request, *args, **kwargs)


class CvDetail(DetailView):
    model = Person
    context_object_name = 'person'
    pk_url_kwarg = 'person_id'
    template_name = 'job/cv_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CvDetail, self).get_context_data(**kwargs)
        context['residence'] = self.object.residence_address_set.all().first()
        context['educations'] = self.object.education_set.all().order_by('start_date')
        context['experiences'] = self.object.experience_set.all().order_by('exp_start_date')
        context['history'] = self.object.cvstate_set.all().order_by('date')
        context['change_status'] = CvStateForm()
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CvDetail, self).dispatch(request, *args, **kwargs)


class CvUpdate(UpdateView):
    model = Person
    context_object_name = 'person'
    pk_url_kwarg = 'person_id'
    template_name = 'job/cv_update.html'
    form_class = CvPersonForm

    def get(self, request, *args, **kwargs):
        print('in GET')
        return super(CvUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('in POST')
        return super(CvUpdate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        print('in FORM_VALID')
        ExperienceInlineFormSet = inlineformset_factory(
            self.model,
            Experience,
            form=CvExperienceForm,
            extra=0)

        EducationInlineFormSet = inlineformset_factory(
            self.model,
            Education,
            form=CvEducationForm,
            extra=0
        )
        formRes = CvResidenceForm(self.request.POST, instance=self.object.residence_address_set.all().first())
        exp_formset = ExperienceInlineFormSet(self.request.POST, instance=self.object, prefix = 'experience')
        edu_formset = EducationInlineFormSet(self.request.POST, instance=self.object, prefix = 'education')
        EduFormSet = formset_factory(EducationForm, extra=0)
        edu_add_set = EduFormSet(self.request.POST, prefix='eduadd')
        ExpFormSet = formset_factory(ExpirienceForm, extra=0)
        exp_add_set = ExpFormSet(self.request.POST, prefix='expadd')
        if formRes.is_valid() and exp_formset.is_valid() and edu_formset.is_valid()\
                and edu_add_set.is_valid() and exp_add_set.is_valid():
            print("Valid addition FORM")
            if self.object.residence_address_set.all():
                formRes.save_init()
            else:
                formRes.save(self.object)

            print('EXP add from', exp_add_set)
            for eduform in edu_add_set:
                if eduform.has_changed():
                    eduform.save(self.object)
            for expform in exp_add_set:
                print('FORMMMMMMM exp', expform)
                if expform.has_changed():
                    expform.save(self.object)

            edu_formset.save()
            exp_formset.save()

        else:
            return super(CvUpdate, self).form_invalid(form)
        return super(CvUpdate, self).form_valid(form)

    def form_invalid(self, form):
        print('INVALID')
        return super(CvUpdate, self).form_invalid(form)


    def get_form(self, form_class=None):
        return super(CvUpdate, self).get_form()

    def get_success_url(self):
        return reverse('manage_form:cv_list')

    def get_context_data(self, **kwargs):
        print('CONTEXT')
        context = super(CvUpdate, self).get_context_data(**kwargs)

        ExperienceInlineFormSet = inlineformset_factory(
            self.model,
            Experience,
            form=CvExperienceForm,
            extra=0)

        EducationInlineFormSet = inlineformset_factory(
            self.model,
            Education,
            form=CvEducationForm,
            extra=0
        )
        data_raw = {'{}-TOTAL_FORMS': '1', '{}-INITIAL_FORMS': '1', '{}-MAX_NUM_FORMS': ''}
        data_eduadd = {k.format('eduadd'): v for k, v in data_raw.items()}
        data_expadd = {k.format('expadd'): v for k, v in data_raw.items()}

        EduFormSet = formset_factory(EducationForm, extra=0)
        edu_add_set = EduFormSet(data_eduadd, prefix='eduadd')
        ExpFormSet = formset_factory(ExpirienceForm, extra=0)
        exp_add_set = ExpFormSet(data_expadd, prefix='expadd')
        if self.request.method == 'POST':
            print('IN POST CONTEXT DATA')
            context['formRes'] = CvResidenceForm(self.request.POST, instance=self.object.residence_address_set.all().first())
            exp_formset = ExperienceInlineFormSet(self.request.POST, instance=self.object, prefix = 'experience')
            edu_formset = EducationInlineFormSet(self.request.POST, instance=self.object, prefix = 'education')
        else:
            exp_formset = ExperienceInlineFormSet(instance=self.object, prefix = 'experience')
            edu_formset = EducationInlineFormSet(instance = self.object, prefix = 'education')

        context['formRes'] = CvResidenceForm(instance=self.object.residence_address_set.all().first())
        context['exp_formset'] = exp_formset
        context['edu_formset'] = edu_formset
        context['exp_add_set'] = exp_add_set
        context['edu_add_set'] = edu_add_set
        return context


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CvUpdate, self).dispatch(request, *args, **kwargs)


@login_required
def ajax_change_state(request, person_id):
    try:
        person = Person.objects.get(pk=person_id)
    except ObjectDoesNotExist as msg:
        return HttpResponseNotFound(msg)
    print(request.method, request.is_ajax())
    if request.method == "POST" and request.is_ajax():
        state_form = CvStateForm(request.POST)
        data = {'action': ''}
        if state_form.is_valid():
            obj_state = state_form.save(commit=False)
            obj_state.cv = person
            obj_state.user_set = request.user
            obj_state.save()
            # new_service_form = ServiceForm()
            # form = render_to_string('repair/ajax/ajax_add_service_form.html',
            #                         context={'service_form': new_service_form, 'order_id': order.id}, request=request)
            # tr = render_to_string('repair/ajax/ajax_add_service_tr.html',
            #                       context={'order_id': order.id, "service": obj_service}, request=request)
            # msg = "*{}* ДОБАВИЛ работу по заказу. Заказ -{}-{}-{}-".format(request.user.get_full_name(), order.order_barcode, order.client.client_name, order.device_name)
            # logger.info(msg)
            data['action'] = 'ok'
        else:
            # form = render_to_string('repair/ajax/ajax_add_service_form.html',
            #                         context={'service_form': service_form, 'order_id': order.id}, request=request)
            data['action'] = "error"
        return JsonResponse(data)
    return HttpResponseNotFound()