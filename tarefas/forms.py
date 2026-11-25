from django import forms


class PeriodoForm(forms.Form):
    inicio = forms.DateField(required=False)
    fim = forms.DateField(required=False)


def filtrar_periodo(request, qs):
    form = PeriodoForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['inicio']:
            qs = qs.filter(prazo__gte=form.cleaned_data['inicio'])
        if form.cleaned_data['fim']:
            qs = qs.filter(prazo__lte=form.cleaned_data['fim'])
    return qs
