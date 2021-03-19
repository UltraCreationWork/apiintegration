def detailform(request):
    form = DetailForm(request.POST or request.GET or None)  
    if 'n' in request.GET:
        qs = Patient_detail.objects.filter(name__icontains=request.GET.get('n'))
        names = list()
        for pd in qs:
            names.append(pd.name)
        return JsonResponse(names, safe=False)    
    elif 'p' in request.GET:
        qs = Patient_detail.objects.filter(procedure__icontains=request.GET.get('p'))
        procedure = list()
        for pd in qs:
            procedure.append(pd.procedure)
        return JsonResponse(procedure, safe=False)
    elif 'q' in request.GET:
        rs = Patient_detail.objects.filter(reffered_by__icontains=request.GET.get('q'))
        refs = list()
        for rf in rs:
            refs.append(rf.reffered_by)
        return JsonResponse(refs, safe=False)
    if form.is_valid():
        form.save()
        return redirect('detail/')
    else:
        data = {
            'form':form
        }
        return render(request,'patient_detail/bootform.html',data)