from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, DetailView, ListView
from .forms import EmployeeForm, SkillForm, SkillFormset
from .models import Employee, Skill


class Home(TemplateView):
    """
    This view is used to display the home page of the website.
    """
    template_name = 'home.html'


class SkillCreateView(CreateView):
    """
    This view is used to create skill using skill form.
    """
    form_class = SkillForm
    template_name = 'skill/skill_create.html'
    success_url = reverse_lazy('task1:skill_list')


class SkillListView(ListView):
    """
    This view will display list of skills in order of new skill at top.
    """
    model = Skill
    template_name = 'skill/skill_list.html'
    queryset = Skill.objects.all().order_by('-created')
    context_object_name = 'skills'


class SkillUpdateView(UpdateView):
    """
    This view is used to update skills.
    """
    model = Skill
    form_class = SkillForm
    template_name = 'skill/skill_create.html'
    success_url = reverse_lazy('task1:skill_list')


class SkillDeleteView(DeleteView):
    """
    This view is used to delete skills.
    """
    model = Skill
    template_name = 'skill/skill_delete.html'
    success_url = reverse_lazy('task1:skill_list')


class EmployeeCreateView(CreateView):
    """
    This view is used to create employee using employee form.
    """
    form_class = EmployeeForm
    template_name = 'employee/employee_create.html'
    success_url = reverse_lazy('task1:employee_list')

    def get_context_data(self, **kwargs):
        """
        This method should pass extra context form and formset to template.
        """
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        context['formset'] = SkillFormset()
        return context

    def post(self, request, *args, **kwargs):
        """
        This method should check whether form and formset are valid or not.
        """
        form_class = self.get_form_class()  # Return the form class to use in this view.
        form = self.get_form(form_class)  # Return an instance of the form to be used in this view.
        formset = SkillFormset(self.request.POST)  # Return the inline formset in this view.
        if form.is_valid() and formset.is_valid():  # Checks whether form and formset are valid or not.
            return self.form_valid(form, formset)  # Save the associated data.

    def form_valid(self, form, formset):
        """
        This method should save the data of form and formset.
        """
        instance = form.save(commit=False)  # Return an object that hasn't yet been saved to the database.
        instance.save()  # Saving an object that hasn't yet been saved to the database.
        form.save()  # Saving the data of form.
        formset.instance = instance  # Saving the instance to the formset.
        formset.save()  # Saving the data of formset.
        return super().form_valid(form)  # Returns an object that represents the parent class.


class EmployeeListView(ListView):
    """
    This view will display list of employees in order of new employee at top.
    """
    model = Employee
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        """
        This method should return queryset of employees.
        """
        query = self.request.GET.get('search')  # Getting the entered data from the search box.
        if query:  # Checks whether the search query is entered or not, else will return all objects.
            queryset = Employee.objects.filter(
                Q(employee_name__icontains=query) | Q(skill__skill_name__icontains=query)
            )
            return queryset
        else:
            return Employee.objects.all().order_by('-created')


class EmployeeUpdateView(UpdateView):
    """
    This view is used to update employees.
    """
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/employee_create.html'
    success_url = reverse_lazy('task1:employee_list')

    def get_context_data(self, **kwargs):
        """
        This method should pass extra context form and formset with instance of object to template.
        """
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = SkillFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = SkillFormset(instance=self.object)
        return context

    def form_valid(self, form):
        """
        This method should save the data of form and formset.
        """
        context = self.get_context_data()  # Returns the context to use in this view.
        formset = context['formset']  # Assigning formset context to formset variable.
        if form.is_valid() and formset.is_valid():  # Checks whether the form and formset are valid or not.
            form.save()  # Saving the form data.
            formset.save()  # Saving the formset data.
        return super().form_valid(form)  # Returns an object that represents the parent class.


class EmployeeDeleteView(DeleteView):
    """
    This view is used to delete employees.
    """
    model = Employee
    template_name = 'employee/employee_delete.html'
    success_url = reverse_lazy('task1:employee_list')


class EmployeeDetailView(DetailView):
    """
    This view will show the details of employee.
    """
    model = Employee
    template_name = 'employee/employee_detail.html'
    context_object_name = 'employee'
